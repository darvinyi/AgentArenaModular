import os
import subprocess
import pandas as pd

def download_attachments(uid: str, root_dir: str) -> None:
    """
    Downloads attachments associated with a given UID and saves them in a UID-specific folder.
    
    Args:
        uid (str): The UID to fetch attachments for
        root_dir (str): The root directory where the UID-specific folder will be created
    """
    # Create UID-specific directory
    uid_dir = os.path.join(root_dir, uid)
    os.makedirs(uid_dir, exist_ok=True)
    
    # Change to the UID directory for downloads
    original_dir = os.getcwd()
    os.chdir(uid_dir)
    
    try:
        url_first = f"https://swagger.prod.platform.usw2.upwork/proxy/openingsV2DS/openings/{uid}/opening-attachments"
        cmd_first = f"curl -s -H 'Accept: application/json' {url_first} | jq .attachments[].uid"

        stream = os.popen(cmd_first)
        UUIDs = stream.read()
        UUIDs = UUIDs.split("\n")
        UUIDs = [uuid.replace('"','') for uuid in UUIDs if uuid]

        for uuid in UUIDs:
            url_second = f"https://swagger.prod.platform.usw2.upwork/proxy/fileStorageDS/files/{uuid}"
            cmd_second = f"curl -s -H 'Accept: application/json' {url_second} | jq -r .link"

            stream = os.popen(cmd_second)
            url_third = stream.read().replace("\n",'')

            executable = ['script', '-q', '/dev/null', "wget", url_third]
            p = subprocess.Popen(executable, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _err = p.communicate()
            output = str(output)
            
            # Extract filename from wget output
            if "Saving to:" in output:
                name_orig = str(output.split("Saving to:")[1].split("\n")[0].strip().encode('utf8'))
                print(f"Downloaded file: {name_orig}")
                name_new = name_orig.split('filename="')[1].split('";')[0]
                print(f"Renaming to: {name_new}")
                
                # Get the most recently created file in the current directory
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                if not files:
                    print("No files found in directory")
                    continue
                    
                latest_file = max(files, key=os.path.getctime)
                print(f"Most recently created file: {latest_file}")

                try:
                    os.rename(latest_file, name_new)
                    print(f"Successfully renamed file to: {name_new}")
                except Exception as e:
                    print(f"Error renaming file: {e}")
            else:
                print("No filename found in wget output")
                print(output)
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def download_all_attachments(csv_path: str, root_dir: str) -> None:
    """
    Downloads attachments for all posts that have attachments according to the CSV file.
    
    Args:
        csv_path (str): Path to the CSV file containing post information
        root_dir (str): Root directory where attachments will be saved
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Filter for posts with attachments
    posts_with_attachments = df[df['HAS_ATTACHMENT'] == True]
    
    print(f"Found {len(posts_with_attachments)} posts with attachments")
    
    # Process each post
    for _, row in posts_with_attachments.iterrows():
        uid = str(row['AGORA_POST_ID'])
        print(f"\nProcessing post {uid}")
        try:
            download_attachments(uid, root_dir)
        except Exception as e:
            print(f"Error processing post {uid}: {e}")

if __name__ == "__main__":
    # Example usage
    test_UID = "1886807791342739171"
    root_directory = "data"
    download_attachments(test_UID, root_directory)