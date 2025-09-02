import json
import xml.etree.ElementTree as ET
import yaml
Path = "Splitting\\"
# Split JSON file into tow files
with open(Path+"file.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    json1 = data[:5]
    json2 = data[5:]

with open(Path+"students_part1.json", "w", encoding="utf-8") as f1:
    json.dump(json1, f1, indent=2)
with open(Path+"students_part2.json", "w", encoding="utf-8") as f2:
    json.dump(json2, f2, indent=2)

# Split XML file into tow files
def split_xml(elements, filename):
    root = ET.Element(Path+"file")
    for el in elements:
        root.append(el)
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

tree = ET.parse(Path+"file.xml")
all_students = list(tree.getroot())

split_xml(all_students[:5], Path+"students_part1.xml")
split_xml(all_students[5:], Path+"students_part2.xml")

# Split YAML file into tow files
with open(Path+"file.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
    yaml1 = data[:5]
    yaml2 = data[5:]

with open(Path+"students_part1.yaml", "w", encoding="utf-8") as f1:
    yaml.dump(yaml1, f1, allow_unicode=True)
with open(Path+"students_part2.yaml", "w", encoding="utf-8") as f2:
    yaml.dump(yaml2, f2, allow_unicode=True)
