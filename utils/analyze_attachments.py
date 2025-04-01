import os
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

def analyze_data_directory(root_dir):
    # Initialize counters
    extension_counts = Counter()
    dir_file_counts = Counter()
    
    # Walk through the data directory
    data_dir = Path(root_dir)
    for root, dirs, files in os.walk(data_dir):
        # Skip the root directory itself
        if root == str(data_dir):
            continue
            
        # Count files in this directory
        dir_file_counts[root] = len(files)
        
        # Count extensions
        for file in files:
            if file.startswith('.'):  # Skip hidden files
                continue
            ext = os.path.splitext(file)[1].lower()
            if ext:  # Only count if there's an extension
                extension_counts[ext] += 1
    
    # Create the extension distribution plot
    plt.figure(figsize=(12, 6))
    
    # Sort extensions by count in descending order
    sorted_extensions = sorted(extension_counts.items(), key=lambda x: x[1], reverse=True)
    extensions = [ext for ext, _ in sorted_extensions]
    counts = [count for _, count in sorted_extensions]
    
    plt.bar(extensions, counts)
    plt.title('File Extension Distribution (Sorted by Count)')
    plt.xlabel('Extension')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('extension_distribution.png')
    plt.close()
    
    # Create the directory size distribution plot
    plt.figure(figsize=(12, 6))
    
    # Count how many directories have each number of files
    size_distribution = Counter(dir_file_counts.values())
    
    # Get the maximum number of files in any directory
    max_files = max(size_distribution.keys())
    
    # Create a bar plot of the distribution
    plt.bar(range(1, max_files + 1), [size_distribution[i] for i in range(1, max_files + 1)])
    plt.title('Distribution of Directory Sizes')
    plt.xlabel('Number of Files in Directory')
    plt.ylabel('Number of Directories')
    plt.tight_layout()
    plt.savefig('directory_size_distribution.png')
    plt.close()
    
    # Print summary statistics
    print("\nFile Extension Summary (Sorted by Count):")
    for ext, count in sorted_extensions:
        print(f"{ext}: {count} files")
    
    print("\nDirectory Size Summary:")
    print(f"Total directories: {len(dir_file_counts)}")
    print(f"Average files per directory: {sum(dir_file_counts.values()) / len(dir_file_counts):.2f}")
    print(f"Max files in a directory: {max(dir_file_counts.values())}")
    print(f"Min files in a directory: {min(dir_file_counts.values())}")
    print("\nDirectory Size Distribution:")
    for size in sorted(size_distribution.keys()):
        print(f"Directories with {size} file{'s' if size != 1 else ''}: {size_distribution[size]}")

if __name__ == "__main__":
    analyze_data_directory("data")
