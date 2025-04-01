import pandas as pd
import os

def process_links(csv_path):
    """
    Process a CSV file containing job postings with removed links and reinsert them.
    
    Args:
        csv_path (str): Path to the input CSV file
        
    Returns:
        dict: Dictionary mapping POST_KEY to descriptions with reinserted links
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Create a dictionary to store descriptions with reinserted links
    post_descriptions = {}
    
    # Group by POST_KEY to handle multiple links per post
    for post_key, group in df.groupby('POST_KEY'):
        description = group.iloc[0]['DESCRIPTION']
        
        # Replace each "(link removed)" with the corresponding link
        for _, row in group.iterrows():
            description = description.replace('(link removed)', row['LINK'], 1)
        
        post_descriptions[post_key] = description
    
    # Create a new DataFrame with reinserted links
    result_df = df.drop_duplicates(subset=['POST_KEY'])[['POST_KEY', 'TITLE', 'DESCRIPTION']]
    result_df['DESCRIPTION'] = result_df['POST_KEY'].map(post_descriptions)
    
    # Save the new CSV file
    output_path = os.path.splitext(csv_path)[0] + '_reinserted.csv'
    result_df.to_csv(output_path, index=False)
    
    return post_descriptions

def reinsert_links(csv_main, csv_links):
    """
    Use a csv file with link information to reinsert links into the main csv.

    Args:
        csv_main (str): Path to the main .csv file.
        csv_links (str): Path to the .csv file with the link information.

    Saves a version of the main .csv file with links.
    """
    # Get dictionary of descriptions with reinserted links
    post_descriptions = process_links(csv_links)
    
    # Read the main CSV file
    df_main = pd.read_csv(csv_main)
    
    # Update descriptions using the dictionary, keeping original descriptions for missing keys
    df_main['DESCRIPTION'] = df_main['POST_KEY'].map(lambda x: post_descriptions.get(x, df_main[df_main['POST_KEY'] == x]['DESCRIPTION'].iloc[0]))
    
    # Save the new CSV file with "_links" appended
    output_path = os.path.splitext(csv_main)[0] + '_links.csv'
    df_main.to_csv(output_path, index=False)
    
    return df_main

if __name__ == "__main__":
    # Example usage
    csv_main = "data/df_randomized_attachment.csv"
    csv_links = "data/df_links.csv"
    descriptions = reinsert_links(csv_main, csv_links)