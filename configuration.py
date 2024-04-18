import csv
import os
import subprocess
from ruamel.yaml import YAML



# Function to convert "True" and "False" strings to boolean
def convert_to_boolean(value):
    if value == "True":
        return True
    elif value == "False":
        return False
    return value



# Function to update specific variables in the YAML file using ruamel.yaml
def update_yaml_file_ruamel(file_path, updates):
    yaml = YAML()
    yaml.preserve_quotes = True
    with open(file_path, 'r') as file:
        content = yaml.load(file)

    # Update the keys with the new values, converting booleans
    for key, new_value in updates.items():
        content[key] = convert_to_boolean(new_value)

    with open(file_path, 'w') as file:
        yaml.dump(content, file)



# Paths setup
## Path to the  raw_data
data_path = '/bulk/IMCbinf_bulk/sbagheri/Projects_IMC/femmicro_test/test_several_db/raw_data'


## Path to the analysis
analysis_path = '/bulk/IMCbinf_bulk/sbagheri/Projects_IMC/femmicro_test/test_several_db/analysis'


## Path to your CSV file
csv_file_path = '/bulk/IMCbinf_bulk/sbagheri/Projects_IMC/femmicro_test/test_several_db/info_structure.csv'


## URL of the Git repository to clone
git_repo_url = 'https://github.com/SycuroLab/FemMicro16S.git'


# Ensure analysis directory exists
if not os.path.exists(analysis_path):
    os.makedirs(analysis_path)
    print("'analysis' directory created")


# Process CSV file
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dir_name = row['dir']
        full_dir_path = os.path.join(analysis_path, dir_name)

        if not os.path.exists(full_dir_path):
            os.makedirs(full_dir_path)
            print(f"Directory {full_dir_path} created")
        else:
            print(f"Directory {full_dir_path} already exists")

        os.chdir(full_dir_path)
        # Check if the '.git' directory exists in the expected repository location
        if not os.path.exists(os.path.join(full_dir_path, 'FemMicro16S')):
            try:
                # The directory does not exist as a Git repository, proceed with cloning
                subprocess.run(['git', 'clone', git_repo_url], check=True)
                print(f"Repository cloned into {dir_name}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to clone repository into {dir_name}: {e}")
        else:
            print(f"Repository already exists, skipping cloning for {dir_name}.")

        config_path = os.path.join(full_dir_path, 'FemMicro16S', 'config.yaml')
        if os.path.exists(config_path):
            updates = {header: row[header] for header in reader.fieldnames if header not in ['dir', 'study']}
            update_yaml_file_ruamel(config_path, updates)
            print(f"Updated config.yaml for {dir_name}")
        else:
            print(f"config.yaml not found for {dir_name}")

        # Run the prepare.py script with subprocess
        os.chdir(os.path.join(full_dir_path, 'FemMicro16S'))
        prepare_script_path = "utils/scripts/common/prepare.py"
        data_specific_path = os.path.join(data_path, dir_name)
        if not os.path.exists(os.path.join(full_dir_path, 'FemMicro16S', 'samples/samples.tsv')):
            subprocess.run(['python', prepare_script_path, data_specific_path], check=True)
            print(f"prepare.py script executed for {dir_name}")
        else:
            print(f"sample list for {dir_name} already exists")

        # Important: Change back to the analysis directory before proceeding to the next iteration
        os.chdir(os.path.join(analysis_path,dir_name,'FemMicro16S'))

        # Prepare the command string
        commands = """
        bash -c "source /home/sahar.bagheri1/softwares/miniconda/etc/profile.d/conda.sh &&
        conda activate snakemake &&
        sbatch dada2_sbatch.sh"
        """
        
        # Execute commands
        try:
            result = subprocess.run(commands, shell=True, check=True, text=True, capture_output=True)
            print("Job submission commands executed successfully.")
            print("Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("An error occurred while trying to execute the commands.")
            print("Error:", e.stderr)



print("Script completed.")

