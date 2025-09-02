
# Step 1: Read the file content into a list
with open("Modifying files\\Modifying_text_file.txt", "r") as f:
    lines = f.readlines()

# Step 2: Insert a new line between line 2 and 3 (i.e., after index 1)
lines.insert(2, "new inserted line\n")

# Step 3: Modify the original second line (which is known at index 1)
lines[1] = "corrected second line\n"

# Replace the typo in any line it appears (in an unknown line)
lines = [line.replace("fourt", "fourth") for line in lines]

# Modify each line by adding a prefix and a suffix
lines = ["START " + line.strip() + " END\n" for line in lines]

# Step 6: Write the updated content back to the file
with open("Modifying files\\Modifying_text_file.txt", "w") as f:
    f.writelines(lines)
