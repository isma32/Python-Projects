# Import necessary libraries
import csv
import json
import openpyxl
import xml.etree.ElementTree as ET
import yaml
# Define the directory
directory = 'Create Files\\'

# 1. Creating a TXT File
with open(directory+'example.txt', 'w') as file:
    file.write("This is a TXT file.")

# 2. Creating a CSV File
with open('directory+'example.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Age'])  # Writing header
    writer.writerow(['Mohamed', 40])
    writer.writerow(['Ali', 30])

# 4. Creating a JSON File
data_json = {"name": "Mohamed", "age": 40}
with open(directory+'example.json', 'w') as file:
    json.dump(data_json, file)

# 3. Creating an XLSX File
wb = openpyxl.Workbook()
sheet = wb.active
sheet['A1'] = 'Name'
sheet['B1'] = 'Age'
sheet['A2'] = 'Mohamed'
sheet['B2'] = 40
wb.save(directory+'example.xlsx')

# 5. Creating an XML File
root = ET.Element("person")
name = ET.SubElement(root, "name")
name.text = "Mohamed"
age = ET.SubElement(root, "age")
age.text = "40"
tree = ET.ElementTree(root)
tree.write(directory+'example.xml")

# 6. Creating a YAML File
data_yaml = {'name': 'Mohamed', 'age': 40}
with open(directory+'example.yaml', 'w') as file:
    yaml.dump(data_yaml, file)

