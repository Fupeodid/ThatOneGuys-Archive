import argparse
import UnityPy
import zipfile
import os
import shutil
import subprocess

def extract_apk(apk_path, extract_dir):
    print(f"Extracting {apk_path} to {extract_dir}")
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

def analyze_environment(apk_dir):
    data_file_path = os.path.join(apk_dir, 'assets', 'bin', 'Data', 'data.unity3d')
    print(f"Loading Unity environment from {data_file_path}")
    
    if not os.path.isfile(data_file_path):
        print(f"Error: Unity environment file {data_file_path} not found.")
        return

    # Load the Unity environment
    unity_env = UnityPy.load(data_file_path)

    # Prepare the log file
    with open("changes.txt", 'w') as output_file:
        for obj_index in range(len(unity_env.objects)):
            obj = unity_env.objects[obj_index]
            if obj.type.name == "GameObject":
                data = obj.read()
                if hasattr(data, 'm_IsActive'):
                    status = "Active" if data.m_IsActive else "Inactive"
                    output_file.write(f"{data.name} > {status}\n")
                    print(f"Found {status} GameObject: {data.name}")

def main(apk_name):
    apk_file = os.path.join(os.getcwd(), apk_name)
    print(f"APK File: {apk_file}")

    if not os.path.isfile(apk_file):
        print(f"Error: {apk_name} does not exist in the same directory as the script")
        return

    extract_dir = apk_file[:-4]
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)  # removes the extracted stuff so it saves storage

    extract_apk(apk_file, extract_dir)
    analyze_environment(extract_dir)

    # Open the changes log
    if os.name == 'posix':
        subprocess.Popen(["xdg-open", "changes.txt"])
    elif os.name == 'nt':
        subprocess.Popen(["start", "changes.txt"], shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze the gameobjects.")
    parser.add_argument("apk_name", help="erm name of the apk")

    args = parser.parse_args()

    main(args.apk_name)
