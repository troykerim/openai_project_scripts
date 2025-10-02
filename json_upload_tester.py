import json

path = r"C:\Users\troyk\OneDrive\Documents\Recykool WM Project\HWTVLM\training.jsonl"

with open(path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        try:
            json.loads(line)
        except Exception as e:
            print(f"Line {i} is invalid: {e}")
