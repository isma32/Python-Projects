import json
import csv
import yaml
import xml.etree.ElementTree as ET
from openpyxl import Workbook
import os


# Define the directory
directory = 'Writing to Files\\'
# Ensure the directory exists
os.makedirs("Writing to Files", exist_ok=True)

# 1. Write to a TXT file
with open(directory+"example.txt", 'w') as f:
    f.write("This is a text file.\nWritten using Python.")


# 2. Write to a CSV file
with open(directory+"example.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Mohamed", 22])
    writer.writerow(["Ali", 25])

# 4. Write to a JSON file
data_json = {
    "students": [
        {"name": "Mohamed", "age": 22},
        {"name": "Ali", "age": 25}
    ]
}
with open(directory+"example.json", 'w') as f:
    json.dump(data_json, f, indent=4)

# 6. Write to a YAML file
data_yaml = {
    "students": [
        {"name": "Mohamed", "age": 22},
        {"name": "Ali", "age": 25}
    ]
}
with open("Writing to Files/example.yaml", 'w') as f:
    yaml.dump(data_yaml, f)

# 5. Write to an XML file
root = ET.Element("students")
ET.SubElement(root, "student", name="Mohamed", age="22")
ET.SubElement(root, "student", name="Ali", age="25")
tree = ET.ElementTree(root)
tree.write(directory+"example.xml")

# 3. Write to an XLSX file
workbook = Workbook()
sheet = workbook.active
sheet.title = "Students"
sheet.append(["Name", "Age"])
sheet.append(["Mohamed", 22])
sheet.append(["Ali", 25])
workbook.save(directory+"example.xlsx")

print("All files created and written successfully.")
