# Create TXT file
Path = "Splitting\\"

# Split TXT
with open(Path+"file.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    part1 = lines[:5]
    part2 = lines[5:]

with open(Path+"students_part1.txt", "w", encoding="utf-8") as f1:
    f1.writelines(part1)
with open(Path+"students_part2.txt", "w", encoding="utf-8") as f2:
    f2.writelines(part2)
