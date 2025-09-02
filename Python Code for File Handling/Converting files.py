import csv
import json
import yaml
import xml.etree.ElementTree as ET
import pandas as pd

# Step 1: Read and parse the text file
students = []
with open("Converting\\file.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(", ")
        student = {kv.split(": ")[0]: kv.split(": ")[1] for kv in parts}
        students.append(student)

# Step 2: Save to CSV
with open("Converting\\file.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows(students)

# Step 3: Save to XLSX
df = pd.DataFrame(students)
df.to_excel("Converting\\file.xlsx", index=False)

# Step 4: Save to JSON
with open("Converting\\file.json", "w", encoding="utf-8") as f:
    json.dump(students, f, indent=2, ensure_ascii=False)

# Step 5: Save to XML
root = ET.Element("Converting\\file")
for s in students:
    student_elem = ET.SubElement(root, "student")
    for key, val in s.items():
        ET.SubElement(student_elem, key).text = val
tree = ET.ElementTree(root)
tree.write("Converting\\file.xml", encoding="utf-8", xml_declaration=True)

# Step 6: Save to YAML
with open("Converting\\file.yaml", "w", encoding="utf-8") as f:
    yaml.dump(students, f, allow_unicode=True, sort_keys=False)
