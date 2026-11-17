import yaml
from google.oauth2 import service_account
from googleapiclient.discovery import build

with open("config.yaml") as f:
    config = yaml.safe_load(f)
landing = config["landing"]

creds = service_account.Credentials.from_service_account_file(
    landing["credentials_path"],
    scopes=["https://www.googleapis.com/auth/drive"],
)
drive = build("drive", "v3", credentials=creds)

# Find the landing subfolder inside the parent folder
query = (
    f"'{landing['folder_id']}' in parents "
    f"and name = '{landing['incoming_subfolder']}' "
    "and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
)
folders = drive.files().list(q=query, fields="files(id, name)").execute()["files"]
landing_id = folders[0]["id"]

# List the files inside landing
query = f"'{landing_id}' in parents and trashed = false"
files = drive.files().list(q=query, fields="files(id, name, size)").execute()["files"]

for f in files:
    print(f["name"], f["id"], f.get("size"))