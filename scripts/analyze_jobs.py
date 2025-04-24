import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# File path
name_csv = "phase1_data/data_v1_superset_without_attachments_combined_labeled_v9_feasible_cleaned.csv"

# Read the CSV file
df = pd.read_csv(name_csv)

# Set the style for better visualizations
plt.style.use('ggplot')
sns.set(rc={'figure.figsize': (12, 8)})

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Plot for CATEGORY - L1 (Bar chart)
l1_counts = df['CATEGORY - L1'].value_counts()
l1_counts.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title('Distribution of CATEGORY - L1', fontsize=14)
ax1.set_xlabel('Category', fontsize=12)
ax1.set_ylabel('Count', fontsize=12)
ax1.tick_params(axis='x', rotation=45, labelsize=10)
ax1.tick_params(axis='y', labelsize=10)

# Plot for CATEGORY - L2 (Pie chart)
l2_counts = df['CATEGORY - L2'].value_counts()

# Get top 10 categories and create an "Other" category
top_10_categories = l2_counts.head(10)
other_count = l2_counts[10:].sum()

# Create a new Series with top 10 + Other
l2_with_other = pd.concat([top_10_categories, pd.Series({'Other': other_count})])

# Create a function to format the labels with both percentage and count
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(pct*total/100.0)
        return f'{pct:.1f}%\n({val})'
    return my_autopct

# Define colors for the pie chart
colors = ['#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#99ccff', 
          '#ffb366', '#ff99ff', '#99ffcc', '#ffb3b3', '#b3ff99', '#ff9999']
# The last color (#ff9999) is for the "Other" category

# Plot the pie chart with top 10 + Other
l2_with_other.plot(kind='pie', ax=ax2, autopct=make_autopct(l2_with_other), startangle=90, colors=colors)
ax2.set_title('CATEGORY - L2 Distribution (Top 10 + Other)', fontsize=14)
ax2.set_ylabel('')  # Remove y-label for pie chart

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the figure
plt.savefig('category_distribution.png', dpi=300, bbox_inches='tight')
print("Visualization saved as 'category_distribution.png'")

# Display some statistics
print("\nCATEGORY - L1 Statistics:")
print(l1_counts)
print("\nCATEGORY - L2 Statistics (Top 10 + Other):")
print(l2_with_other)
print("\nAll CATEGORY - L2 Statistics:")
print(l2_counts)