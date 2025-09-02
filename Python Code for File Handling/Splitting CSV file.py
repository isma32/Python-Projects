import csv

# Split CSV
Path = "Splitting\\"

with open(Path+"file.csv", "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]
    part1, part2 = data[:5], data[5:]

for idx, part in enumerate([part1, part2], 1):
    with open(Path+f"students_part{idx}.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(part)
