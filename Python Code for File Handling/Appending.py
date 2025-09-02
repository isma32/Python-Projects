import json 
import csv
import yaml
import xml.etree.ElementTree as ET
from openpyxl import Workbook
import os

# Ensure the directory exists
os.makedirs("Appending", exist_ok=True)

# 1. Append to a TXT file
with open("Appending/example.txt", 'a') as f:
    f.write("Amina and Arraf\n")

# 2. Append to a CSV file
with open("Appending/example.csv", 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Amina", 20])
    writer.writerow(["Arraf", 22])
    
# 3. Append to an XLSX file
workbook = Workbook()
sheet = workbook.active
sheet.append(["Amina", 20])
sheet.append(["Arraf", 22])
workbook.save("Appending/example.xlsx")

# 4. Append to a JSON file
with open("Appending/example.json", 'r+') as f:
    data_json = json.load(f)
    # Append new data
    data_json["students"].append({"name": "Amina", "age": 20})
    data_json["students"].append({"name": "Arraf", "age": 22})
    f.seek(0)  # Move back to the beginning of the file to overwrite
    json.dump(data_json, f, indent=4)
    
# 5. Append to an XML file
tree = ET.parse("Appending/example.xml")
root = tree.getroot()
ET.SubElement(root, "student", name="Amina", age="20")
ET.SubElement(root, "student", name="Arraf", age="22")
tree.write("Appending/example.xml")

# 6. Append to a YAML file
with open("Appending/example.yaml", 'a') as f:
    data_yaml = {
        "students": [
            {"name": "Amina", "age": 20},
            {"name": "Arraf", "age": 22}
        ]
    }
    yaml.dump(data_yaml, f)
