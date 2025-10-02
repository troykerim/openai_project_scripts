'''
Helper script that will combine Gmail URLs + label values into the proper jsonl file 

'''
import json
import os

URLS_FILE = r""   # path to your URLs txt file
LABELS_FILE = r"" # path to your labels txt file
OUTPUT_JSONL = r""   # output JSONL file

# common extensions to strip
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"]


def normalize_name(name):
    """Remove brackets and common image extensions"""
    name = name.strip("[]")  # remove square brackets
    base, ext = os.path.splitext(name)
    if ext.lower() in IMAGE_EXTS:
        return base
    return name


def parse_urls_file(path):
    """Parse image urls file into {basename: file_id}"""
    mapping = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            # Example: [image.jpg] https://drive.google.com/uc?id=FILEID
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            name = parts[0]
            url = parts[1]
            if "id=" in url:
                file_id = url.split("id=")[1]
                base = normalize_name(name)
                mapping[base] = file_id
    return mapping


def parse_labels_file(path):
    """Parse labels file into {basename: label_data}"""
    mapping = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            first_bracket = line.find("[")
            last_bracket = line.find("]")
            name = line[first_bracket+1:last_bracket]
            base = normalize_name(name)
            label_data = line[last_bracket+1:].strip()
            mapping[base] = label_data
    return mapping


def main():
    urls_map = parse_urls_file(URLS_FILE)
    labels_map = parse_labels_file(LABELS_FILE)

    count = 0
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as out:
        for base, file_id in urls_map.items():
            if base in labels_map:
                label_data = labels_map[base]

                obj = {
                    "messages": [
                        {"role": "system",
                         "content": "You are an assistant that detects the material of waste objects based on vision."},
                        {"role": "user",
                         "content": "Please detect the objects with label 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 in the image and output their bounding boxes."},
                        {"role": "user",
                         "content": [
                             {"type": "image_url",
                              "image_url": {
                                  "url": f"https://drive.google.com/uc?export=download&id={file_id}",
                                  "detail": "high"}}
                         ]},
                        {"role": "assistant",
                         "content": label_data}
                    ]
                }
                out.write(json.dumps(obj, ensure_ascii=False) + "\n")
                count += 1
            else:
                print(f"No label found for {base}")

    print(f"Wrote {count} matched entries to {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()