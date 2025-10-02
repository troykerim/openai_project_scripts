# Parses the label info for each image into a single line and outputs a text file.
from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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
            pageSize=1000,
            pageToken=page_token
        ).execute()

        items = results.get("files", [])
        all_files.extend(items)

        page_token = results.get("nextPageToken")
        if not page_token:
            break

    return all_files


def list_labels_in_subfolders(service, folder_id):
    """Recursively find all .txt label files inside 'labels' subfolders"""
    all_labels = []

    subfolders = list_files_with_pagination(service, folder_id)

    for sub in subfolders:
        if sub["mimeType"] == "application/vnd.google-apps.folder":
            if sub["name"].lower() == "labels":
                # Collect label files
                files = list_files_with_pagination(service, sub["id"])
                for f in files:
                    if f["name"].lower().endswith(".txt"):  # label file
                        all_labels.append(f)
            else:
                all_labels.extend(list_labels_in_subfolders(service, sub["id"]))

    return all_labels


def download_label_file(service, file_id):
    """Download the contents of a label file as text"""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return fh.getvalue().decode("utf-8")


def main():
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    # Collect all label files
    all_labels = list_labels_in_subfolders(service, DATASET_FOLDER_ID)

    with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as out:
        for lbl in all_labels:
            file_content = download_label_file(service, lbl["id"]).strip()
            if not file_content:
                continue  # skip empty label files

            # Preserve newlines inside the string using \n
            formatted_content = file_content.replace("\n", "\\n")

            # Strip extension to get base image name
            image_name = os.path.splitext(lbl["name"])[0]

            # Write to output file
            out.write(f"[{image_name}] {formatted_content}\n")

    print(f"Saved {len(all_labels)} label files to {OUTPUT_TEXT_FILE}")


if __name__ == "__main__":
    main()
