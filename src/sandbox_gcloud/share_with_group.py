from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import pickle
import argparse
import csv

# スコープを変更
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
TOKEN_PICKLE_FILE = 'token.pickle'

def get_credentials():
    """認証情報を取得"""
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def share_with_group(service, file_id, group_email, role='reader'):
    """
    ファイルをグループと共有する
    
    Args:
        service: Google Drive API サービス
        file_id: 共有するファイルのID
        group_email: 共有先のグループのメールアドレス
        role: 権限（'reader', 'commenter', 'writer'）
    """
    try:
        # グループの権限を設定
        permission = {
            'type': 'group',
            'role': role,
            'emailAddress': group_email
        }
        
        # 権限を追加（通知なし）
        result = service.permissions().create(
            fileId=file_id,
            body=permission,
            fields='id',
            sendNotificationEmail=False
        ).execute()
        
        print(f"ファイルをグループ {group_email} と共有しました。")
        print(f"権限: {role}")
        return True
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return False

def read_file_ids_from_csv(csv_file):
    """CSVファイルからファイルIDを読み込む"""
    file_ids = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_ids.append(row['ID'])
    return file_ids

def main():
    parser = argparse.ArgumentParser(description='Google Driveのファイルをグループと共有')
    parser.add_argument('--csv', help='ファイルIDが含まれるCSVファイルのパス')
    parser.add_argument('--file-id', help='共有するファイルのID')
    parser.add_argument('group_email', help='共有先のグループのメールアドレス')
    parser.add_argument('--role', choices=['reader', 'commenter', 'writer'],
                      default='writer', help='共有する権限（デフォルト: writer）')
    args = parser.parse_args()

    if not args.csv and not args.file_id:
        parser.error("--csv または --file-id のいずれかを指定してください")

    # 認証情報を取得
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # ファイルIDの取得
    file_ids = []
    if args.csv:
        file_ids = read_file_ids_from_csv(args.csv)
    else:
        file_ids = [args.file_id]

    # 各ファイルをグループと共有
    for file_id in file_ids:
        print(f"\nファイルID: {file_id}")
        share_with_group(service, file_id, args.group_email, args.role)

if __name__ == '__main__':
    main() 