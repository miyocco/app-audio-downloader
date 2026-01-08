import sys
import yt_dlp
import os
from pathlib import Path
import getpass

# デスクトップを保存先に設定
DOWNLOAD_DIR = Path.home() / "Desktop"

def download_radiko(url, output_template=None, cookie_file=None, credentials=None):
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

    print("\n--- 認証設定 (プレミアム会員向け) ---")
    print("1: メールアドレスとパスワードを入力 (推奨)")
    print("2: クッキーファイル (cookies.txt) を使用")
    print("3: 認証なし (無料会員)")
    
    auth_choice = input("選択 [3]: ").strip()
    
    cookie_file_path = None
    credentials = None

    if auth_choice == '1':
        print("\nRadikoプレミアムのログイン情報を入力してください。")
        email = input("メールアドレス: ").strip()
        password = getpass.getpass("パスワード: ")
        if email and password:
            credentials = (email, password)
        else:
            print("情報が不足しています。認証なしで続行します。")
            
    elif auth_choice == '2':
        print("\nNetscape形式のクッキーファイル（cookies.txt）のパスを入力してください。")
        print("（ブラウザ拡張機能 'Get cookies.txt' 等でエクスポートできます）")
        path_input = input("ファイルパス: ").strip()
        # パスの引用符などを除去
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
    # 引数がある場合は従来通り処理
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        out_tmpl = sys.argv[2] if len(sys.argv) > 2 else None
        print(f"Downloading from: {target_url}")
        print(f"Destination: {DOWNLOAD_DIR}")
        
        # 引数モードでのクッキー利用は簡易的に未対応
        download_radiko(target_url, out_tmpl)
    else:
        # 引数がない場合は対話モード
        interactive_mode()