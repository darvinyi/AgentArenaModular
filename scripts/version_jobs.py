import pandas as pd
import openai
import time
from tqdm import tqdm
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_job_version(title, description, sector, experience_level, projected_value, skills):
    """Analyze a job posting to determine its version (v1-v5) using GPT-4."""
    
    prompt = f"""Analyze this job posting and classify it as v1, v2, v3, v4, or v5 based on the following criteria:

v1: Can be completed with just the job description and public files, no client clarification needed.  v1 jobs can not necessitate an ongoing relationship with the client.  There has to be a simple handoff of requirements and then a single returning of results.
v2: Requires a few clarification questions but no proprietary data or ongoing interaction.  v2 jobs can not necessitate an ongoing relationship with the client (except for the few clarification questions).  There has to be a simple handoff of requirements and then a single returning of results.
v3: Requires ongoing interaction with the client for feedback and check-ins
v4: Requires proprietary data to complete the job
v5: Requires access to essential tools and data sources from the client

Job Details:
Title: {title}
Description: {description}
Sector: {sector}
Experience Level: {experience_level}
Projected Value: {projected_value}
Skills Required: {skills}

Respond with ONLY the version number (v1, v2, v3, v4, or v5)."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a job classification expert. Respond with only the version number."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error analyzing job: {e}")
        return "ERROR"

def main():
    # Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv('df_randomized.csv')
    
    # Limit to first 100 rows
    #df = df.head(100)
    
    # Add version column
    df['JOB_VERSION'] = None
    
    # Process each row
    print("Analyzing job descriptions...")
    for idx in tqdm(df.index):
        row = df.iloc[idx]
        version = analyze_job_version(
            row['TITLE'],
            row['DESCRIPTION'],
            row['SECTOR'],
            row['EXPERIENCE_LEVEL'],
            row['PROJECTED_VALUE'],
            row['SKILLS_AND_EXPERTISE']
        )
        df.at[idx, 'JOB_VERSION'] = version
        
        # Add a small delay to avoid rate limits
        time.sleep(1)
    
    # Save the results
    print("Saving results...")
    df.to_csv('df_randomized_versioned.csv', index=False)
    print("Done!")

if __name__ == "__main__":
    main()
