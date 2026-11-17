import yaml
from google.oauth2 import service_account
from googleapiclient.discovery import build

with open("config.yaml") as f:
    landing = yaml.safe_load(f)["landing"]

creds = service_account.Credentials.from_service_account_file(
    landing["credentials_path"],
    scopes=["https://www.googleapis.com/auth/drive"],
)
drive = build("drive", "v3", credentials=creds)

# 1. Can the bot see the configured folder at all?
folder = drive.files().get(fileId=landing["folder_id"], fields="id, name").execute()
print("Configured folder:", folder["name"])

# 2. What is inside it?
items = drive.files().list(
    q=f"'{landing['folder_id']}' in parents and trashed = false",
    fields="files(name, mimeType)",
).execute()["files"]
for item in items:
    print(" -", item["name"], "|", item["mimeType"])