from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
import csv
import sys

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('drive', 'v3', credentials=creds)

results = service.files().list(
    q="sharedWithMe",
    fields="files(id, name, mimeType, owners, createdTime, shared, sharingUser)"
).execute()

# CSVヘッダーを定義
fieldnames = ['ファイル名', 'ID', 'オーナー名', 'オーナーメールアドレス', 'オーナー組織', '共有者名', '共有者メールアドレス', '共有者組織', '作成日']

# CSVファイルに書き込み
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

for f in results.get("files", []):
    created_time = datetime.fromisoformat(f['createdTime'].replace('Z', '+00:00'))
    
    # オーナー情報の取得
    owner = f.get('owners', [{}])[0] if f.get('owners') else {}
    owner_name = owner.get('displayName', '不明')
    owner_email = owner.get('emailAddress', '不明')
    owner_org = owner.get('organizations', [{}])[0].get('name', '不明') if owner.get('organizations') else '不明'
    
    # 共有者情報の取得
    sharing_user = f.get('sharingUser', {})
    sharing_name = sharing_user.get('displayName', '不明')
    sharing_email = sharing_user.get('emailAddress', '不明')
    sharing_org = sharing_user.get('organizations', [{}])[0].get('name', '不明') if sharing_user.get('organizations') else '不明'
    
    writer.writerow({
        'ファイル名': f['name'],
        'ID': f['id'],
        'オーナー名': owner_name,
        'オーナーメールアドレス': owner_email,
        'オーナー組織': owner_org,
        '共有者名': sharing_name,
        '共有者メールアドレス': sharing_email,
        '共有者組織': sharing_org,
        '作成日': created_time.strftime('%Y-%m-%d %H:%M:%S')
    })
