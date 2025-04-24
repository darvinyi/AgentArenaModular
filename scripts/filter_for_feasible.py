import pandas as pd

name_csv = 'phase1_data/data_v1_superset_without_attachments_2_labeled_v9.csv'

# Read the input CSV file
df = pd.read_csv(name_csv)#, skiprows=range(1, 892))  # Keep header row, skip rows 1-892

# Count non-empty values in Deliverables column
deliverables_count = df['Deliverable'].notna().sum()
print(f"\nNumber of rows with Deliverables: {deliverables_count}")

# Split the dataframe based on v1 Feasible column
df_feasible = df[df['v1 Feasible'] == True]
df_not_feasible = df[df['v1 Feasible'] == False]

# Save the split dataframes to separate CSV files
df_feasible.to_csv(name_csv[:-4] + "_feasible.csv", index=False)
df_not_feasible.to_csv(name_csv[:-4] + "_not_feasible.csv", index=False)

# Print summary statistics
print(f"Total posts: {len(df)}")
print(f"Feasible posts: {len(df_feasible)}")
print(f"Not feasible posts: {len(df_not_feasible)}")
