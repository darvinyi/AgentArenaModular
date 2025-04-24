import pandas as pd

# Read the CSV files
df1 = pd.read_csv('data_v1_superset.csv')
df2 = pd.read_csv('posts_without_attachments - posts_without_attachments_labeled.csv')

# Filter df1 for rows where HAS_ATTACHMENT is False
df1_no_attachments = df1[df1['HAS_ATTACHMENT'] == False]

# Get unique POST_KEYs from each file
keys1 = set(df1_no_attachments['POST_KEY'])
keys2 = set(df2['POST_KEY'])

# Find keys that are in df1 but not in df2
unique_to_df1 = keys1 - keys2
# Find keys that are in df2 but not in df1
unique_to_df2 = keys2 - keys1

print("\nPOST_KEYs unique to data_v1_superset.csv (where HAS_ATTACHMENT is False):")
for key in sorted(unique_to_df1):
    print(key)

print("\nPOST_KEYs unique to posts_without_attachments_labeled.csv:")
for key in sorted(unique_to_df2):
    print(key)

print(f"\nSummary:")
print(f"Total rows in data_v1_superset.csv: {len(df1)}")
print(f"Rows with HAS_ATTACHMENT=False in data_v1_superset.csv: {len(df1_no_attachments)}")
print(f"Total unique keys in filtered data_v1_superset.csv: {len(keys1)}")
print(f"Total unique keys in posts_without_attachments_labeled.csv: {len(keys2)}")
print(f"Keys only in filtered data_v1_superset.csv: {len(unique_to_df1)}")
print(f"Keys only in posts_without_attachments_labeled.csv: {len(unique_to_df2)}")
