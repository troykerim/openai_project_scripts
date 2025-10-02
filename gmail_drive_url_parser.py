# Gmail URL parser 
from __future__ import print_function
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Path to your OAuth credentials file
CLIENT_SECRET_FILE = r""  
OUTPUT_TEXT_FILE = r""  
DATASET_FOLDER_ID = ""  


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def list_files_with_pagination(service, folder_id):
    """List ALL files in a folder, handling pagination"""
    all_files = []
    page_token = None

    while True:
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000,  # max allowed per call
            pageToken=page_token
        ).execute()

        items = results.get("files", [])
        all_files.extend(items)

        page_token = results.get("nextPageToken")
        if not page_token:
            break

    return all_files


def list_images_in_subfolders(service, folder_id):
    """Recursively find all image files inside subfolders named 'images'"""
    all_files = []

    subfolders = list_files_with_pagination(service, folder_id)

    for sub in subfolders:
        if sub["mimeType"] == "application/vnd.google-apps.folder":
            if sub["name"].lower() == "images":
                # List all files in this "images" folder
                files = list_files_with_pagination(service, sub["id"])
                for f in files:
                    all_files.append({
                        "image_name": f["name"],
                        "url": f"https://drive.google.com/uc?id=" + f["id"]
                    })
            else:
                # Recurse deeper into subfolders
                all_files.extend(list_images_in_subfolders(service, sub["id"]))

    return all_files


def main():
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    # Collect all image files
    all_images = list_images_in_subfolders(service, DATASET_FOLDER_ID)

    # Write results to text file
    with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as f:
        for item in all_images:
            f.write(f"[{item['image_name']}] {item['url']}\n")

    print(f"Saved {len(all_images)} image URLs to {OUTPUT_TEXT_FILE}")


if __name__ == "__main__":
    main()