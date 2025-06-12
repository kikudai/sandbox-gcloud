# Google Drive 共有ファイル一覧取得ツール

このツールは、Google Driveで共有されているファイルの一覧を取得し、CSV形式で出力するPythonスクリプトです。

## 前提条件

- Python 3.6以上
- Googleアカウント
- Google Cloud Platformのプロジェクト

## セットアップ手順

1. Google Cloud Platformでプロジェクトを作成し、Google Drive APIを有効化します：
   - [Google Cloud Console](https://console.cloud.google.com/)にアクセス
   - 新しいプロジェクトを作成
   - 「APIとサービス」→「ライブラリ」から「Google Drive API」を検索して有効化

2. 認証情報を作成します：
   - Google Cloud Consoleの「APIとサービス」→「認証情報」に移動
   - 「認証情報を作成」→「OAuth 2.0 クライアントID」を選択
   - アプリケーションの種類で「デスクトップアプリケーション」を選択
   - クライアントIDとクライアントシークレットが生成される
   - 認証情報をダウンロードし、`credentials.json`として保存

3. 必要なPythonパッケージをインストールします：
   ```bash
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

## 使用方法

1. `credentials.json`をスクリプトと同じディレクトリに配置します。

2. スクリプトを実行します：
   ```bash
   python googledrivelist.py > output.csv
   ```

3. 初回実行時は、ブラウザが開きGoogleアカウントでの認証が求められます。
   - アカウントを選択
   - 必要な権限を承認

4. 認証が完了すると、共有ファイルの一覧がCSV形式で`output.csv`に出力されます。

## 出力される情報

CSVファイルには以下の情報が含まれます：
- ファイル名
- ファイルID
- オーナー名
- オーナーのメールアドレス
- オーナーの組織名
- 共有者名
- 共有者のメールアドレス
- 共有者の組織名
- 作成日

## 注意事項

- 組織情報やメールアドレスは、APIの権限設定やユーザーのプライバシー設定によっては取得できない場合があります。
- 取得できない情報は「不明」と表示されます。
- 認証情報（`credentials.json`）は機密情報です。GitHubなどにアップロードしないよう注意してください。

## その他
BOM付きファイルにしたいとき
```bash
sed -i '1s/^/\xef\xbb\xbf/' output.csv
```