# Google Drive ツール集

このリポジトリには、Google Driveを操作するための複数のツールが含まれています。

## 使用方法

すべてのツールは`main.py`から利用できます：

```bash
# ヘルプの表示
python main.py --help

# 共有ファイル一覧の取得
python main.py list-files
python main.py list-files -o output.csv

# ファイルの共有
python main.py share --file-id "ファイルID" "グループメールアドレス"
python main.py share --csv "file_ids.csv" "グループメールアドレス"
```

## 1. 共有ファイル一覧取得ツール

Google Driveで共有されているファイルの一覧を取得し、CSV形式で出力するツールです。

### 使用方法

```bash
# 標準出力に出力
python main.py list-files

# ファイルに出力
python main.py list-files -o output.csv
```

### 出力される情報

CSVファイルには以下の情報が含まれます：
- ファイル名
- ファイルID
- オーナー名
- オーナーのメールアドレス
- 共有者名
- 共有者のメールアドレス
- アクセス権
- 作成日
- 共有リンク

### 注意事項

- 組織情報やメールアドレスは、APIの権限設定やユーザーのプライバシー設定によっては取得できない場合があります。
- 取得できない情報は「不明」と表示されます。

### その他

BOM付きファイルにしたいとき
```bash
sed -i '1s/^/\xef\xbb\xbf/' output.csv
```

## 2. ファイル共有ツール

Google Driveのファイルをグループと共有するためのツールです。

### 使用方法

#### 単一ファイルの共有

```bash
python main.py share --file-id "ファイルID" "グループメールアドレス"
```

#### 複数ファイルの共有（CSVファイルから）

```bash
python main.py share --csv "ファイルID一覧.csv" "グループメールアドレス"
```

#### オプション

- `--role`: 共有権限を指定（デフォルト: writer）
  - `reader`: 閲覧者のみ
  - `commenter`: コメント可能
  - `writer`: 編集可能

#### 使用例

1. ファイルを編集者権限で共有:
```bash
python main.py share --file-id "1abc...xyz" "group@example.com"
```

2. ファイルを閲覧者権限で共有:
```bash
python main.py share --file-id "1abc...xyz" "group@example.com" --role reader
```

3. CSVファイルから複数ファイルを共有:
```bash
python main.py share --csv "file_ids.csv" "group@example.com"
```

#### CSVファイル形式

ファイルIDを読み込むCSVファイルは以下の形式である必要があります：

```csv
ID
1abc...xyz
2def...uvw
```

## セットアップ

### 前提条件

- Python 3.6以上
- Google Cloud Platformのプロジェクト設定
- uv（高速なPythonパッケージインストーラー）

### インストール手順

1. uvのインストール（まだインストールしていない場合）:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 必要なパッケージをインストール:
```bash
uv pip install -r requirements.txt
```

3. Google Cloud Consoleで認証情報を設定:
   - Google Cloud Consoleでプロジェクトを作成
   - Google Drive APIを有効化
   - OAuth 2.0クライアントIDを作成
   - 認証情報を`credentials.json`としてダウンロード
   - `credentials.json`をスクリプトと同じディレクトリに配置

## 共通の注意事項

- 初回実行時はブラウザでGoogleアカウントの認証が必要です
- 認証情報は`token.pickle`に保存されます
- 共有時は通知メールは送信されません
- 認証情報（`credentials.json`）は機密情報です。GitHubなどにアップロードしないよう注意してください。