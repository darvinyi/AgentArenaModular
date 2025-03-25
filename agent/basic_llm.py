import os
import random
from typing import Optional
import openai
from api.data import AgentArenaData

class BasicLLMAgent:
    def __init__(self, api_key: str, data: AgentArenaData):
        """
        Initialize the BasicLLMAgent with OpenAI API key and data handler.
        
        Args:
            api_key (str): OpenAI API key
            data (AgentArenaData): Instance of AgentArenaData for job processing
        """
        self.api_key = api_key
        self.data = data
        openai.api_key = api_key
        
        # System prompt for job processing
        self.system_prompt = """You are a professional freelancer who has been given a job to complete.
        Your task is to provide a detailed response that solves this job.  Do your best to solve the job
        and give an output that is sufficient to finish the job.  You only have one shot."""
    
    def process_jobs(self, output_dir: str = "output") -> None:
        """
        Process all available jobs using a random selection process.
        
        Args:
            output_dir (str): Directory to save job outputs
        """
        # Get all job metadata
        jobs_metadata = self.data.get_jobs_metadata()
        
        for job_id, (title, sector, skills, exp_level, budget, country) in jobs_metadata.items():
            # Randomly decide whether to take the job (50% chance)
            if random.random() < 0.5:
                print(f"Agent decided to take job {job_id}: {title}")
                
                # Get the job description
                job_description = self.data.get_job_description(job_id)
                
                try:
                    # Make API call to OpenAI
                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": f"Job Title: {title}\nSector: {sector}\nSkills Required: {skills}\nExperience Level: {exp_level}\nBudget: ${budget:,.2f}\nCountry: {country}\n\nJob Description:\n{job_description}"}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    # Extract the response
                    output = response.choices[0].message.content
                    
                    # Submit the job output
                    saved_path = self.data.submit_job(
                        save_dir=output_dir,
                        model_name="simpleLLM",
                        job_id=job_id,
                        output=output
                    )
                    
                    print(f"Successfully processed job {job_id}. Output saved to: {saved_path}")
                    
                except Exception as e:
                    print(f"Error processing job {job_id}: {str(e)}")
            else:
                print(f"Agent decided not to take job {job_id}: {title}")

# Example usage
if __name__ == "__main__":
    # Initialize the data handler
    data = AgentArenaData("data/df_randomized_feasible_cleaned.csv")
    
    # Initialize the agent with your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    agent = BasicLLMAgent(api_key, data)
    
    # Process all jobs
    agent.process_jobs()
