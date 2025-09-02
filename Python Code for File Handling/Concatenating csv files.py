import yaml

# File paths
file1 = "Concatenating Files\\file1.yaml"
file2 = "Concatenating Files\\file2.yaml"
file3 = "Concatenating Files\\merged_file3.yaml"

# Load the content of both YAML files
with open(file1, 'r') as f1, open(file2, 'r') as f2:
    data1 = yaml.safe_load(f1)
    data2 = yaml.safe_load(f2)

# Concatenate the data assuming the structure is a list of dictionaries
merged_data = data1 + data2

# Write the merged data into a new YAML file
with open(file3, 'w') as out:
    yaml.dump(merged_data, out)



