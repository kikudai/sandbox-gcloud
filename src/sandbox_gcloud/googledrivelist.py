from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import csv
import sys
import os
import pickle
import argparse

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
TOKEN_PICKLE_FILE = 'token.pickle'

def get_credentials():
    creds = None
    # トークンファイルが存在する場合は読み込む
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # 有効な認証情報がない場合は新規認証
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 認証情報を保存
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_basic_permission(service, file_id):
    """ファイルの基本的なアクセス権を取得"""
    try:
        file = service.files().get(
            fileId=file_id,
            fields='capabilities(canEdit,canComment)'
        ).execute()
        
        capabilities = file.get('capabilities', {})
        if capabilities.get('canEdit'):
            return '編集者'
        elif capabilities.get('canComment'):
            return '閲覧者（コメント可）'
        else:
            return '閲覧者'
    except Exception as e:
        return '不明'

def main():
    parser = argparse.ArgumentParser(description='Google Driveの共有ファイル一覧を取得')
    args = parser.parse_args()

    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q="sharedWithMe",
        fields="files(id, name, mimeType, owners, createdTime, shared, sharingUser, webViewLink)"
    ).execute()

    # CSVヘッダーを定義
    fieldnames = ['ファイル名', 'ID', 'オーナー名', 'オーナーメールアドレス', '共有者名', '共有者メールアドレス', 'アクセス権', '作成日', '共有リンク']

    # CSVファイルに書き込み
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for f in results.get("files", []):
        created_time = datetime.fromisoformat(f['createdTime'].replace('Z', '+00:00'))
        
        # オーナー情報の取得
        owner = f.get('owners', [{}])[0] if f.get('owners') else {}
        owner_name = owner.get('displayName', '不明')
        owner_email = owner.get('emailAddress', '不明')
        
        # 共有者情報の取得
        sharing_user = f.get('sharingUser', {})
        sharing_name = sharing_user.get('displayName', '不明')
        sharing_email = sharing_user.get('emailAddress', '不明')
        
        # アクセス権情報の取得
        access_rights = get_basic_permission(service, f['id'])
        
        writer.writerow({
            'ファイル名': f['name'],
            'ID': f['id'],
            'オーナー名': owner_name,
            'オーナーメールアドレス': owner_email,
            '共有者名': sharing_name,
            '共有者メールアドレス': sharing_email,
            'アクセス権': access_rights,
            '作成日': created_time.strftime('%Y-%m-%d %H:%M:%S'),
            '共有リンク': f.get('webViewLink', '不明')
        })

if __name__ == '__main__':
    main()
