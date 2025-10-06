import os
import xml.etree.ElementTree as ET

input_folder = r""      # Folder containing your 54 XML files
output_folder = r""  # Folder where .txt files will be saved

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all XML files in the input folder
for filename in os.listdir(input_folder):
    if not filename.endswith(".xml"):
        continue

    xml_path = os.path.join(input_folder, filename)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Prepare output text file path (same name as XML, but .txt extension)
    txt_filename = os.path.splitext(filename)[0] + ".txt"
    txt_path = os.path.join(output_folder, txt_filename)

    # Collect all bounding boxes and names
    lines = []
    for obj in root.findall("object"):
        name = obj.find("name").text.strip()
        bndbox = obj.find("bndbox")
        xmin = bndbox.find("xmin").text.strip()
        xmax = bndbox.find("xmax").text.strip()
        ymin = bndbox.find("ymin").text.strip()
        ymax = bndbox.find("ymax").text.strip()
        lines.append(f"{name} {xmin} {xmax} {ymin} {ymax}")

    # Write lines to text file
    with open(txt_path, "w") as f:
        f.write("\n".join(lines))

print(f"Done! Created {len(os.listdir(output_folder))} text files in: {output_folder}")