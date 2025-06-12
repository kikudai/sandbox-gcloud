#!/usr/bin/env python3

import click
import sys
import logging
from sandbox_gcloud.googledrivelist import main as list_main
from sandbox_gcloud.share_with_group import main as share_main

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group(invoke_without_command=True)
def cli():
    """Google Drive ツール集"""
    logger.debug("CLIグループが呼び出されました")
    pass

@cli.command(name='list-files')
@click.option('--output', '-o', help='出力ファイル名（デフォルト: 標準出力）')
def list_files(output):
    """共有ファイル一覧を取得"""
    logger.debug(f"list_filesコマンドが呼び出されました。output={output}")
    try:
        if output:
            logger.debug(f"出力ファイルを開きます: {output}")
            sys.stdout = open(output, 'w', encoding='utf-8')
        logger.debug("list_mainを呼び出します")
        # sys.argvを更新して、googledrivelist.pyのargparseが正しく動作するようにする
        original_argv = sys.argv
        sys.argv = [sys.argv[0]]  # プログラム名のみを残す
        list_main()
        sys.argv = original_argv  # 元のsys.argvに戻す
    except Exception as e:
        logger.error(f"list_filesでエラーが発生しました: {str(e)}", exc_info=True)
        raise

@cli.command(name='share')
@click.option('--csv', help='ファイルIDが含まれるCSVファイルのパス')
@click.option('--file-id', help='共有するファイルのID')
@click.option('--role', type=click.Choice(['reader', 'commenter', 'writer']),
              default='writer', help='共有する権限（デフォルト: writer）')
@click.argument('group_email')
def share(csv, file_id, role, group_email):
    """ファイルをグループと共有"""
    logger.debug(f"shareコマンドが呼び出されました。csv={csv}, file_id={file_id}, role={role}, group_email={group_email}")
    try:
        # share_mainに引数を渡すために、sys.argvを更新
        original_argv = sys.argv
        sys.argv = [sys.argv[0]]  # プログラム名のみを残す
        if csv:
            logger.debug(f"CSVファイルを指定: {csv}")
            sys.argv.extend(['--csv', csv])
        if file_id:
            logger.debug(f"ファイルIDを指定: {file_id}")
            sys.argv.extend(['--file-id', file_id])
        sys.argv.append(group_email)
        if role:
            logger.debug(f"権限を指定: {role}")
            sys.argv.extend(['--role', role])
        logger.debug(f"更新後のsys.argv: {sys.argv}")
        logger.debug("share_mainを呼び出します")
        share_main()
        sys.argv = original_argv  # 元のsys.argvに戻す
    except Exception as e:
        logger.error(f"shareでエラーが発生しました: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    try:
        logger.debug("プログラムを開始します")
        logger.debug(f"コマンドライン引数: {sys.argv}")
        cli()
    except Exception as e:
        logger.error(f"メイン処理でエラーが発生しました: {str(e)}", exc_info=True)
        click.echo(f"エラーが発生しました: {str(e)}", err=True)
        sys.exit(1)
