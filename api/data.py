import pandas as pd
from typing import Dict, Tuple
import os

class AgentArenaData:
    def __init__(self, csv_path: str):
        """
        Initialize AgentArenaData with a CSV file path.
        
        Args:
            csv_path (str): Path to the CSV file containing job data
        """
        self.df = pd.read_csv(csv_path)
    
    def get_num_jobs(self) -> int:
        """
        Returns the total number of jobs in the dataset.
        
        Returns:
            int: Number of jobs (rows) in the dataframe
        """
        return len(self.df)
    
    def get_jobs_metadata(self) -> Dict[int, Tuple[str, str, str, str, float, str]]:
        """
        Returns a dictionary mapping job IDs to their metadata.
        
        Returns:
            Dict[int, Tuple[str, str, str, str, float, str]]: Dictionary with ID as key and
                (TITLE, SECTOR, SKILLS_AND_EXPERTISE, EXPERIENCE_LEVEL, BUDGET, COUNTRY) as value
        """
        metadata_dict = {}
        for _, row in self.df.iterrows():
            metadata_dict[row['ID']] = (
                row['TITLE'],
                row['SECTOR'],
                row['SKILLS_AND_EXPERTISE'],
                row['EXPERIENCE_LEVEL'],
                row['BUDGET'],
                row['COUNTRY']
            )
        return metadata_dict
    
    def get_job_description(self, job_id: int) -> str:
        """
        Returns the description for a specific job ID.
        
        Args:
            job_id (int): The ID of the job
            
        Returns:
            str: The job description
            
        Raises:
            KeyError: If the job_id is not found in the dataset
        """
        job = self.df[self.df['ID'] == job_id]
        if job.empty:
            raise KeyError(f"Job ID {job_id} not found in the dataset")
        return job.iloc[0]['DESCRIPTION']
    
    def submit_job(self, save_dir: str, model_name: str, job_id: int, output: str) -> str:
        """
        Saves the model's output for a specific job to a text file.
        
        Args:
            save_dir (str): Directory to save the output file
            model_name (str): Name of the model that generated the output
            job_id (int): ID of the job
            output (str): The output text to save
            
        Returns:
            str: Path to the saved file
            
        Raises:
            KeyError: If the job_id is not found in the dataset
        """
        # Verify job exists
        if job_id not in self.df['ID'].values:
            raise KeyError(f"Job ID {job_id} not found in the dataset")
        
        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Create filename in format: output_model_jobID.txt
        filename = f"output_{model_name}_{job_id}.txt"
        filepath = os.path.join(save_dir, filename)
        
        # Save the output
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
            
        return filepath

# Example usage:
if __name__ == "__main__":
    # Initialize the data
    data = AgentArenaData("data/df_randomized_feasible_cleaned.csv")
    
    # Print total number of jobs
    print(f"\nTotal number of jobs: {data.get_num_jobs():,}")
    
    # Print metadata for first 3 jobs
    print("\nMetadata for first 3 jobs:")
    metadata = data.get_jobs_metadata()
    for job_id in range(3):
        title, sector, skills, exp_level, budget, country = metadata[job_id]
        print(f"\nJob ID: {job_id}")
        print(f"Title: {title}")
        print(f"Sector: {sector}")
        print(f"Skills: {skills}")
        print(f"Experience Level: {exp_level}")
        print(f"Budget: ${budget:,.2f}" if pd.notna(budget) else "Budget: Not specified")
        print(f"Country: {country}")
    
    # Print description for first job
    print("\nDescription for first job:")
    print("-" * 80)
    print(data.get_job_description(0))
    print("-" * 80)
    
    # Example of submitting a job output
    example_output = "This is an example model output for job 0"
    saved_path = data.submit_job(
        save_dir="outputs",
        model_name="example_model",
        job_id=0,
        output=example_output
    )
    print(f"\nSaved output to: {saved_path}")
