import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('df_randomized_versioned.csv')

# Set style for better visualizations
plt.style.use('default')
sns.set_theme()

# Define ordered versions for consistent color mapping
ordered_versions = ['v1', 'v2', 'v3', 'v4', 'v5']

# Get matplotlib's default colors
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 1. Version Distribution Pie Chart
plt.figure(figsize=(10, 8))
version_counts = df['JOB_VERSION'].value_counts().reindex(ordered_versions)
plt.pie(version_counts, labels=version_counts.index, autopct='%1.1f%%', colors=default_colors)
plt.title('Distribution of Job Versions')
plt.savefig('version_distribution.png')
plt.close()

# 2. Total Projected Value by Version (in thousands)
plt.figure(figsize=(10, 6))
version_values = df.groupby('JOB_VERSION')['PROJECTED_VALUE'].sum().reindex(ordered_versions) / 1000  # Convert to thousands
version_values.plot(kind='bar', color=default_colors)
plt.title('Total Projected Value by Version')
plt.xlabel('Version')
plt.ylabel('Total Projected Value ($K)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('version_values.png')
plt.close()

# 3. Sector Distribution by Version
plt.figure(figsize=(12, 8))
sector_version = pd.crosstab(df['SECTOR'], df['JOB_VERSION'])[ordered_versions]
sector_version.plot(kind='bar', stacked=True, color=default_colors)
plt.title('Sector Distribution by Version')
plt.xlabel('Sector')
plt.ylabel('Number of Jobs')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Version')
plt.tight_layout()
plt.savefig('sector_distribution.png')
plt.close()

# Create sample dataset with first 5 jobs of each version in specified order
sample_jobs = []
for version in ordered_versions:
    version_jobs = df[df['JOB_VERSION'] == version].head(5)
    sample_jobs.append(version_jobs)

# Combine all samples and save to CSV
sample_df = pd.concat(sample_jobs)
sample_df.to_csv('df_randomized_versioned_sample.csv', index=False)

# Print numerical summaries
print("\nJob Version Distribution:")
print(version_counts)
print("\nTotal Projected Value by Version (in thousands):")
print(version_values)
print("\nSector Distribution by Version:")
print(sector_version)
