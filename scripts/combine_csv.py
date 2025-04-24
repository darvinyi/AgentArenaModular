#!/usr/bin/env python3
import pandas as pd
import sys
import os

def combine_csv_files(file1_path, file2_path, output_path):
    """
    Combine two CSV files with the same columns, keeping the first occurrence
    of any duplicate POST_KEY rows.
    
    Args:
        file1_path (str): Path to the first CSV file
        file2_path (str): Path to the second CSV file
        output_path (str): Path to save the combined CSV file
    """
    # Check if files exist
    if not os.path.exists(file1_path):
        print(f"Error: File '{file1_path}' does not exist.")
        return False
    
    if not os.path.exists(file2_path):
        print(f"Error: File '{file2_path}' does not exist.")
        return False
    
    try:
        # Read the CSV files
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        # Check if both dataframes have the same columns
        columns1 = set(df1.columns)
        columns2 = set(df2.columns)
        
        if columns1 != columns2:
            print("Warning: The CSV files have different columns.")
            
            # Find columns unique to each file
            only_in_file1 = columns1 - columns2
            only_in_file2 = columns2 - columns1
            
            if only_in_file1:
                print(f"Columns only in {file1_path}: {sorted(list(only_in_file1))}")
            
            if only_in_file2:
                print(f"Columns only in {file2_path}: {sorted(list(only_in_file2))}")
            
            # Keep only the columns that exist in both files
            common_columns = columns1.intersection(columns2)
            print(f"Keeping only the {len(common_columns)} columns that exist in both files.")
            
            # Filter dataframes to keep only common columns
            df1 = df1[list(common_columns)]
            df2 = df2[list(common_columns)]
        
        # Check if POST_KEY column exists
        if 'POST_KEY' not in df1.columns:
            print("Error: 'POST_KEY' column not found in the CSV files.")
            return False
        
        # Count overlapping POST_KEYs
        post_keys1 = set(df1['POST_KEY'])
        post_keys2 = set(df2['POST_KEY'])
        overlapping_keys = post_keys1.intersection(post_keys2)
        
        print(f"Number of POST_KEYs in first file: {len(post_keys1)}")
        print(f"Number of POST_KEYs in second file: {len(post_keys2)}")
        print(f"Number of overlapping POST_KEYs: {len(overlapping_keys)}")
        
        # Combine the dataframes, keeping the first occurrence of any duplicate POST_KEY
        combined_df = pd.concat([df1, df2], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['POST_KEY'], keep='first')
        
        # Save the combined dataframe to a new CSV file
        combined_df.to_csv(output_path, index=False)
        print(f"Successfully combined CSV files. Output saved to '{output_path}'")
        print(f"Total rows in combined file: {len(combined_df)}")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    
    file1_path = "phase1_data/data_v1_superset_without_attachments_labeled_v9_feasible.csv"
    file2_path = "phase1_data/data_v1_superset_without_attachments_2_labeled_v9_feasible.csv"
    output_path = "phase1_data/data_v1_superset_without_attachments_combined_labeled_v9_feasible.csv"
    
    combine_csv_files(file1_path, file2_path, output_path)

if __name__ == "__main__":
    main()
