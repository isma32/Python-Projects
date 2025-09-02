import csv
import json
import openpyxl
import xml.etree.ElementTree as ET
import yaml

# Define the directory
directory = 'Create Files\\'

# 1. Read TXT File
with open(directory + 'example.txt', 'r') as file:
    txt_content = file.read()
print("\nTXT Content:")
print(txt_content)

# 2. Read CSV File
with open(directory + 'example.csv', 'r') as file:
    reader = csv.reader(file)
    print("\nCSV Content:")
    for row in reader:
        print(row)

# 4. Read JSON File
with open(directory + 'example.json', 'r') as file:
    json_content = json.load(file)
print("\nJSON Content:")
print(json_content)

# 3. Read XLSX File
wb = openpyxl.load_workbook(directory + 'example.xlsx')
sheet = wb.active
print("\nXLSX Content:")
for row in sheet.iter_rows(values_only=True):
    print(row)

# 5. Read XML File
tree = ET.parse(directory + "example.xml")
root = tree.getroot()
print("\nXML Content:")
for person in root.findall('person'):
    name = person.find('name').text
    age = person.find('age').text
    print(f"Name: {name}, Age: {age}")

# 6. Read YAML File
with open(directory + 'example.yaml', 'r') as file:
    yaml_content = yaml.safe_load(file)
print("\nYAML Content:")
print(yaml_content)
