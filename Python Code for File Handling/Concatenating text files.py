# Define the file paths
file1_path = "file1.txt"
file2_path = "file2.txt"
file3_path = "file3.txt"

# Open the output file in write modeCL
with open(file3_path, 'w', encoding='utf-8') as file3_file: 
    # Read and write the content of the first file
    with open(file1_path, 'r', encoding='utf-8') as file1:
        file3_file.write(file1.read())
    # add an empty line
    file3_file.write("\n")
    # Read and write the content of the second file
    with open(file2_path, 'r', encoding='utf-8') as file2:
        file3_file.write(file2.read())
