import pandas as pd
import sys

def find_repeated_post_keys(file1, file2):
    """
    Find the intersection of POST_KEY values between two CSV files.
    
    Args:
        file1 (str): Path to the first CSV file
        file2 (str): Path to the second CSV file
        
    Returns:
        set: The set of repeated POST_KEY values
    """
    try:
        # Read the CSV files
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        # Check if POST_KEY column exists in both dataframes
        if 'POST_KEY' not in df1.columns:
            print(f"Error: 'POST_KEY' column not found in {file1}")
            return set()
        
        if 'POST_KEY' not in df2.columns:
            print(f"Error: 'POST_KEY' column not found in {file2}")
            return set()
        
        # Get the sets of POST_KEY values
        post_keys1 = set(df1['POST_KEY'].dropna())
        post_keys2 = set(df2['POST_KEY'].dropna())
        
        # Find the intersection
        repeated_keys = post_keys1.intersection(post_keys2)
        
        return repeated_keys
    
    except Exception as e:
        print(f"Error: {e}")
        return set()

def main():
    if len(sys.argv) != 3:
        print("Usage: python find_repeats.py <file1.csv> <file2.csv>")
        return
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    repeated_keys = find_repeated_post_keys(file1, file2)
    
    print(f"Total number of repeated POST_KEY elements: {len(repeated_keys)}")
    print("\nRepeated POST_KEY elements:")
    for key in sorted(repeated_keys):
        print(key)

if __name__ == "__main__":
    main()
