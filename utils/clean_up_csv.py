import pandas as pd
import sys
import os
import re

def clean_csv(input_csv_path, output_csv_path=None):
    """
    Clean a CSV file by selecting specific columns and saving to a new file.
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_csv_path (str, optional): Path to save the cleaned CSV. If None, will save in same directory
            as input with '_cleaned' appended to the filename.
    """
    # Check if file exists
    if not os.path.exists(input_csv_path):
        print(f"Error: File {input_csv_path} does not exist")
        return
    
    # Check if file is a CSV
    if not input_csv_path.endswith('.csv'):
        print("Error: Input file must be a CSV file")
        return

    # Generate output path if not provided
    if output_csv_path is None:
        output_csv_path = input_csv_path.rsplit('.csv', 1)[0] + '_cleaned.csv'

    # Read the CSV file
    try:
        df = pd.read_csv(input_csv_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # List of columns to keep
    columns_to_keep = [
        'POST_KEY',
        'AGORA_POST_ID',
        'TITLE',
        'DESCRIPTION',
        'SECTOR',
        'SUBSECTOR',
        'SUBSUBSECTOR',
        'SKILLS_AND_EXPERTISE',
        'EXPERIENCE_LEVEL',
        'CLIENT_RATING',
        'IS_HOURLY',
        'HOURLY_LOW',
        'HOURLY_HIGH',
        'BUDGET',
        'COUNTRY',
        'LANGUAGE',
        'POST_DATE'
    ]

    # Filter columns that exist in the DataFrame
    existing_columns = [col for col in columns_to_keep if col in df.columns]
    
    if not existing_columns:
        print("Error: None of the specified columns found in the CSV file")
        return

    # Select only the specified columns that exist, maintaining the order from columns_to_keep
    df_cleaned = df[existing_columns].reindex(columns=existing_columns)
    
    # Add ID column at the start
    df_cleaned.insert(0, 'ID', range(len(df_cleaned)))

    # Save the cleaned DataFrame
    try:
        df_cleaned.to_csv(output_csv_path, index=False)
        print(f"Successfully saved cleaned data to {output_csv_path}")
        print(f"Columns saved in order: {', '.join(df_cleaned.columns)}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

def rename_data_dirs(csv_path, root_dir):
    """
    Rename directories in root_dir based on mapping between AGORA_POST_ID and POST_KEY from CSV.
    
    Args:
        csv_path (str): Path to the CSV file containing AGORA_POST_ID and POST_KEY mapping
        root_dir (str): Path to the root directory containing folders to rename
    """
    # Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f"Error: CSV file {csv_path} does not exist")
        return
    
    # Check if root directory exists
    if not os.path.exists(root_dir):
        print(f"Error: Root directory {root_dir} does not exist")
        return

    # Read the CSV file
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Verify required columns exist
    required_columns = ['AGORA_POST_ID', 'POST_KEY']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: CSV file must contain columns: {', '.join(required_columns)}")
        return

    # Create mapping dictionary with string conversion
    id_to_key = dict(zip(df['AGORA_POST_ID'].astype(str), df['POST_KEY'].astype(str)))
    
    # Get list of directories in root_dir
    try:
        dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    except Exception as e:
        print(f"Error reading directory {root_dir}: {e}")
        return

    # Rename directories
    renamed_count = 0
    skipped_count = 0
    error_count = 0

    for dir_name in dirs:
        if dir_name in id_to_key:
            old_path = os.path.join(root_dir, dir_name)
            new_path = os.path.join(root_dir, str(id_to_key[dir_name]))
            
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {dir_name} -> {id_to_key[dir_name]}")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming {dir_name}: {e}")
                error_count += 1
        else:
            print(f"Skipped: {dir_name} (no mapping found)")
            skipped_count += 1

    print(f"\nSummary:")
    print(f"Successfully renamed: {renamed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python clean_up_csv.py <input_csv_file> [output_csv_file]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) == 3 else None
        clean_csv(input_file, output_file)
