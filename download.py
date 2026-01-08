import sys
import yt_dlp
import os
from pathlib import Path
import getpass
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# デスクトップを保存先に設定
DOWNLOAD_DIR = Path.home() / "Desktop"

def get_env_credentials():
    """環境変数から認証情報を取得"""
    email = os.getenv("RADIKO_MAIL")
    password = os.getenv("RADIKO_PASSWORD")
    if email and password:
        return email, password
    return None

def download_radiko(url, output_template=None, cookie_file=None, credentials=None):
    # ... (変更なし) ...
    """
    Downloads Radiko audio using yt-dlp.
    
    Args:
        url (str): The Radiko URL.
        output_template (str, optional): Output filename.
        cookie_file (str, optional): Path to cookie file.
        credentials (tuple, optional): (username, password) for Radiko premium.
    """
    
    # 出力パスの設定（デフォルトはデスクトップ）
    if output_template:
        out_path = str(DOWNLOAD_DIR / output_template)
    else:
        out_path = str(DOWNLOAD_DIR / '%(title)s [%(id)s].%(ext)s')

    ydl_opts = {
        'outtmpl': out_path,
        'format': 'bestaudio/best',
    }
    
    # 認証設定
    if cookie_file:
        ydl_opts['cookiefile'] = cookie_file
    
    if credentials:
        ydl_opts['username'] = credentials[0]
        ydl_opts['password'] = credentials[1]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        pass

def interactive_mode():
    print(f"保存先: {DOWNLOAD_DIR}")
    print("RadikoのURLを入力してください。")
    print("（複数ある場合は改行して入力してください。入力完了時は何も入力せずにEnterを押してください）")
    
    urls = []
    while True:
        try:
            line = input("> ").strip()
            if not line:
                break
            urls.append(line)
        except EOFError:
            break
            
    if not urls:
        print("URLが入力されませんでした。終了します。")
        return

    env_creds = get_env_credentials()
    cookie_file_path = None
    credentials = None

    print("\n--- 認証設定 (プレミアム会員向け) ---")
    
    default_choice = '3'
    
    if env_creds:
        print(f"1: 環境変数の設定を使用 ({env_creds[0]}) [推奨]")
        default_choice = '1'
    else:
        print("1: (環境変数の設定なし)")

    print("2: メールアドレスとパスワードを手動入力")
    print("3: クッキーファイル (cookies.txt) を使用")
    print("4: 認証なし (無料会員)")
    
    auth_choice = input(f"選択 [{default_choice}]: ").strip()
    if not auth_choice:
        auth_choice = default_choice
    
    if auth_choice == '1':
        if env_creds:
            credentials = env_creds
            print("環境変数の認証情報を使用します。")
        else:
            print("環境変数が設定されていません。")
            
    elif auth_choice == '2':
        print("\nRadikoプレミアムのログイン情報を入力してください。")
        email = input("メールアドレス: ").strip()
        password = getpass.getpass("パスワード: ")
        if email and password:
            credentials = (email, password)
        else:
            print("情報が不足しています。認証なしで続行します。")
            
    elif auth_choice == '3':
        print("\nNetscape形式のクッキーファイル（cookies.txt）のパスを入力してください。")
        path_input = input("ファイルパス: ").strip()
        path_input = path_input.replace('"', '').replace("'", "")
        if os.path.exists(path_input):
            cookie_file_path = path_input
        else:
            print(f"ファイルが見つかりません: {path_input}")
            print("認証なしで続行します。")

    print(f"\n{len(urls)} 件のダウンロードを開始します...\n")
    
    for url in urls:
        print(f"Processing: {url}")
        download_radiko(url, cookie_file=cookie_file_path, credentials=credentials)
        print("-" * 40)

if __name__ == "__main__":
    # 引数がある場合も環境変数をチェック
    env_creds = get_env_credentials()
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        out_tmpl = sys.argv[2] if len(sys.argv) > 2 else None
        print(f"Downloading from: {target_url}")
        print(f"Destination: {DOWNLOAD_DIR}")
        
        # 環境変数が設定されていれば自動適用
        download_radiko(target_url, out_tmpl, credentials=env_creds)
    else:
        # 引数がない場合は対話モード
        interactive_mode()