import os
import subprocess

test_UID = "1886807791342739171"

url_first = f"https://swagger.prod.platform.usw2.upwork/proxy/openingsV2DS/openings/{test_UID}/opening-attachments"

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

        name_new = name_orig.split('filename="')[1].split('";')[0]
        print(f"Renaming to: {name_new}")
        
        try:
            os.rename(latest_file, name_new)
            print(f"Successfully renamed file to: {name_new}")
        except Exception as e:
            print(f"Error renaming file: {e}")
    else:
        print("No filename found in wget output")
        print(output)