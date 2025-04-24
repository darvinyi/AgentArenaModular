import pandas as pd

name_csv = "df_randomized_attachment_2_links.csv"

# Read the input CSV file
df = pd.read_csv(name_csv)

# Split the dataframe based on HAS_ATTACHMENT column
df_with_attachments = df[df['HAS_ATTACHMENT'] == True]
df_without_attachments = df[df['HAS_ATTACHMENT'] == False]

# Save the split dataframes to separate CSV files
df_with_attachments.to_csv(name_csv[:-4] + '_with_attachments.csv', index=False)
df_without_attachments.to_csv(name_csv[:-4] + '_without_attachments.csv', index=False)

# Print summary statistics
print(f"Total posts: {len(df)}")
print(f"Posts with attachments: {len(df_with_attachments)}")
print(f"Posts without attachments: {len(df_without_attachments)}")
