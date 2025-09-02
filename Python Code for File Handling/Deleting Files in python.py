import os
import csv
import json
import openpyxl
import xml.etree.ElementTree as ET
import yaml

# Define the directory
directory = 'Create Files\\'

# 1. Delete TXT File
txt_file = directory + 'example.txt'
if os.path.exists(txt_file):
    os.remove(txt_file)
    print(f"\n{txt_file} has been deleted.")
else:
    print(f"\n{txt_file} does not exist.")

# 2. Delete CSV File
csv_file = directory + 'example.csv'
if os.path.exists(csv_file):
    os.remove(csv_file)
    print(f"\n{csv_file} has been deleted.")
else:
    print(f"\n{csv_file} does not exist.")

# 4. Delete JSON File
json_file = directory + 'example.json'
if os.path.exists(json_file):
    os.remove(json_file)
    print(f"\n{json_file} has been deleted.")
else:
    print(f"\n{json_file} does not exist.")

# 3. Delete XLSX File
xlsx_file = directory + 'example.xlsx'
if os.path.exists(xlsx_file):
    os.remove(xlsx_file)
    print(f"\n{xlsx_file} has been deleted.")
else:
    print(f"\n{xlsx_file} does not exist.")

# 5. Delete XML File
xml_file = directory + 'example.xml'
if os.path.exists(xml_file):
    os.remove(xml_file)
    print(f"\n{xml_file} has been deleted.")
else:
    print(f"\n{xml_file} does not exist.")

# 6. Delete YAML File
yaml_file = directory + 'example.yaml'
if os.path.exists(yaml_file):
    os.remove(yaml_file)
    print(f"\n{yaml_file} has been deleted.")
else:
    print(f"\n{yaml_file} does not exist.")
