import pandas as pd
import openai
import os
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_job_feasibility(title, description, sector, experience_level, projected_value, skills):
    """Analyze if a job posting can be completed by an AI agent with attachments."""
    
    prompt = f"""Analyze this job posting and determine if it describes a SPECIFIC TASK or PROJECT that an AI agent could complete. 
This should NOT be a general job description for hiring an employee, but rather a clear, specific task or project.

Determine if the SPECIFIC TASK can be completed if the AI agent is given the attachments/files/specifications mentioned in the description. (Answer YES/NO)

Key Requirements for ANY Task:
- Must be a specific, well-defined task or project (not a general job description)
- Must have clear deliverables or end goals
- Must be completable as a standalone project
- Must NOT be an ongoing role or position

The task:
- CAN require specific files or documents mentioned in the description
- Must still NOT require:
  - Additional clarification beyond what's in the files
  - Access to proprietary systems
  - Ongoing interaction or feedback
  - Any materials beyond those explicitly mentioned

Job Details:
Title: {title}
Description: {description}
Sector: {sector}
Experience Level: {experience_level}
Projected Value: {projected_value}
Skills Required: {skills}

Respond with just YES or NO."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing whether jobs can be completed by AI agents. Respond with just YES or NO."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        return result == "YES"
    except Exception as e:
        print(f"Error analyzing job: {e}")
        return False

def filter_csv_for_feasible_jobs(input_csv_path, output_csv_path=None):
    """
    Filter a CSV file to find jobs that can be completed by an AI agent with attachments.
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_csv_path (str, optional): Path to save the filtered CSV. If None, will save in same directory
            as input with '_feasible' appended to the filename.
    """
    # Generate output path if not provided
    if output_csv_path is None:
        base_path = os.path.splitext(input_csv_path)[0]
        output_csv_path = f"{base_path}_feasible.csv"
    
    # Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv(input_csv_path)
    
    # Add feasible column
    df['IS_FEASIBLE'] = False
    
    # Process each row
    print("Analyzing job descriptions...")
    for idx in tqdm(df.index):
        row = df.iloc[idx]
        is_feasible = analyze_job_feasibility(
            row['TITLE'],
            row['DESCRIPTION'],
            row['SECTOR'],
            row['EXPERIENCE_LEVEL'],
            row['PROJECTED_VALUE'],
            row['SKILLS_AND_EXPERTISE']
        )
        df.at[idx, 'IS_FEASIBLE'] = is_feasible
    
    # Filter and save results
    print("Saving results...")
    feasible_df = df[df['IS_FEASIBLE']]
    feasible_df.to_csv(output_csv_path, index=False)
    
    print(f"Done! Found {len(feasible_df)} feasible jobs out of {len(df)} total jobs analyzed.")
    print(f"Results saved to: {output_csv_path}")

if __name__ == "__main__":
    filter_csv_for_feasible_jobs('data/df_randomized.csv')
