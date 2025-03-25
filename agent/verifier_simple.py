import os
import pandas as pd
from typing import Dict, List, Set
from api.data import AgentArenaData
from openai import OpenAI

class SimpleVerifier:
    def __init__(self, openai_api_key: str, data: AgentArenaData):
        """
        Initialize the SimpleVerifier with OpenAI API key and AgentArenaData.
        
        Args:
            openai_api_key (str): OpenAI API key for potential model-based verification
            data (AgentArenaData): The AgentArenaData object containing job information
        """
        self.openai_api_key = openai_api_key
        self.client = OpenAI(api_key=openai_api_key)
        self.data = data
        
    def _read_output_file(self, filepath: str) -> str:
        """Read the contents of an output file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_filename(self, filename: str) -> tuple[str, int]:
        """Parse the model name and job ID from filename."""
        # Expected format: output_{model_name}_{jobID}.txt
        parts = filename.replace('.txt', '').split('_')
        if len(parts) != 3 or parts[0] != 'output':
            raise ValueError(f"Invalid filename format: {filename}")
        return parts[1], int(parts[2])
    
    def _verify_output(self, output: str, job_description: str) -> bool:
        """
        Verify if the output satisfies the job description using GPT-4.
        
        Args:
            output (str): The model's output to verify
            job_description (str): The job description to compare against
            
        Returns:
            bool: True if the output is sufficient to get paid, False otherwise
        """
        prompt = f"""You are a job verification expert. Your task is to determine if the provided output is sufficient to warrant payment for the job.

Job Description:
{job_description}

Output to Verify:
{output}

Please analyze if this output is sufficient to warrant payment for the job. Consider:
1. Does it address the key requirements of the job?
2. Is it complete and well-formed?
3. Does it provide value to the client?

Respond with only "YES" if the output is sufficient to warrant payment, or "NO" if it is not.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a job verification expert. Respond with only YES or NO."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Low temperature for more consistent results
            )
            
            result = response.choices[0].message.content.strip().upper()
            return result == "YES"
            
        except Exception as e:
            print(f"Error during verification: {str(e)}")
            return False  # Fail safe: if there's an error, consider it a failure
    
    def process_outputs(self, output_dir: str) -> None:
        """
        Process all output files and generate results.csv
        
        Args:
            output_dir (str): Directory containing output files
        """
        # Get all txt files in the output directory
        output_files = [f for f in os.listdir(output_dir) 
                       if f.endswith('.txt') and f.startswith('output_')]
        
        # Initialize sets to track unique models and jobs
        model_names: Set[str] = set()
        job_ids: Set[int] = set()
        
        # First pass: collect all model names and job IDs
        for filename in output_files:
            try:
                model_name, job_id = self._parse_filename(filename)
                model_names.add(model_name)
                job_ids.add(job_id)
            except ValueError:
                continue
        
        # Create a DataFrame with all jobs as rows and models as columns
        results_df = pd.DataFrame(index=sorted(job_ids), 
                                columns=sorted(model_names))
        results_df.index.name = 'jobID'
        
        # Second pass: process each file and fill the DataFrame
        for filename in output_files:
            try:
                model_name, job_id = self._parse_filename(filename)
                filepath = os.path.join(output_dir, filename)
                
                # Read the output and job description
                output = self._read_output_file(filepath)
                job_description = self.data.get_job_description(job_id)
                
                # Get job metadata for better logging
                job_metadata = self.data.get_jobs_metadata()[job_id]
                job_title = job_metadata[0]  # First element is the title
                
                # Verify the output
                is_valid = self._verify_output(output, job_description)
                result = 'win' if is_valid else 'fail'
                
                # Update the DataFrame
                results_df.loc[job_id, model_name] = result
                
                # Print detailed information
                print(f"\nJob: {job_title} (ID: {job_id})")
                print(f"Agent: {model_name}")
                print(f"Result: {'✓ SUCCESS' if is_valid else '✗ FAILURE'}")
                print("-" * 80)
                
            except (ValueError, KeyError) as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
        
        # Save the results
        output_path = os.path.join(output_dir, 'results.csv')
        results_df.to_csv(output_path)
        print(f"\nResults saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    # Initialize the data
    data = AgentArenaData("data/df_randomized_feasible_cleaned.csv")
    
    # Create verifier and process outputs
    verifier = SimpleVerifier(
        openai_api_key="your-api-key-here",  # Replace with actual API key
        data=data
    )
    verifier.process_outputs("outputs")
