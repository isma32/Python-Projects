import pandas as pd

# Define file paths
input_path = "Splitting/file.xlsx"
output_path1 = "Splitting/file_part1.xlsx"
output_path2 = "Splitting/file_part2.xlsx"

# Read the Excel file
df = pd.read_excel(input_path)

# Calculate midpoint to split
mid = len(df) // 2

# Split the DataFrame into two parts
df_part1 = df.iloc[:mid]
df_part2 = df.iloc[mid:]

# Save each part to a new Excel file
df_part1.to_excel(output_path1, index=False)
df_part2.to_excel(output_path2, index=False)
