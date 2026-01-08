import sys
import yt_dlp
import os
from pathlib import Path
import tempfile

# デスクトップを保存先に設定
DOWNLOAD_DIR = Path.home() / "Desktop"

def extract_cookies_to_file(browser_name, output_path):
    """
    指定されたブラウザからクッキーを抽出し、ファイルに保存する。
    """
    print(f"[{browser_name}] からクッキーを抽出しています...")
    opts = {
        'cookiesfrombrowser': (browser_name, None, None, None),
        'cookiefile': str(output_path),
        'skip_download': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            # Radikoのトップページにアクセスしてクッキーを確保
            ydl.extract_info("https://radiko.jp", download=False)
        print(f"クッキーを抽出しました: {output_path}")
        return True
    except Exception as e:
        print(f"クッキーの抽出に失敗しました: {e}")
        return False

def download_radiko(url, output_template=None, cookie_file=None):
    """
    Downloads Radiko audio using yt-dlp.
    
    Args:
        url (str): The Radiko URL.
        output_template (str, optional): Output filename template. 
                                         Defaults to 'Desktop/%(title)s [%(id)s].%(ext)s'.
        cookie_file (str, optional): Path to the Netscape formatted cookie file.
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
    
    if cookie_file:
        ydl_opts['cookiefile'] = cookie_file
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        # 対話モードで1つ失敗しても他を続行できるようにsys.exitは削除または制御
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

    # ブラウザのクッキーを使用するか確認（プレミアム会員向け）
    use_cookies = input("Edgeブラウザのログイン情報（クッキー）を使用しますか？ (y/n) [n]: ").strip().lower() == 'y'

    cookie_file_path = None
    if use_cookies:
        # 一時ファイルを作成してクッキーを保存
        # delete=Falseにして、使用後に手動で削除する（Windows等でのファイルロック回避のため念のため）
        tf = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        tf.close()
        cookie_file_path = tf.name
        
        if not extract_cookies_to_file('edge', cookie_file_path):
            print("警告: クッキーの抽出に失敗しました。ログインなしで続行します。")
            os.remove(cookie_file_path)
            cookie_file_path = None

    print(f"\n{len(urls)} 件のダウンロードを開始します...\n")
    
    try:
        for url in urls:
            print(f"Processing: {url}")
            download_radiko(url, cookie_file=cookie_file_path)
            print("-" * 40)
    finally:
        # クリーンアップ
        if cookie_file_path and os.path.exists(cookie_file_path):
            try:
                os.remove(cookie_file_path)
                # print("一時クッキーファイルを削除しました。")
            except:
                pass

if __name__ == "__main__":
    # 引数がある場合は従来通り処理
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        out_tmpl = sys.argv[2] if len(sys.argv) > 2 else None
        print(f"Downloading from: {target_url}")
        print(f"Destination: {DOWNLOAD_DIR}")
        
        # 引数モードでのクッキー利用は簡易的に未対応（必要ならオプション解析を追加）
        # ただし、main.pyを直接叩くユースケースは減っているため、基本はデフォルトで。
        # もし必要ならインタラクティブモードを推奨。
        download_radiko(target_url, out_tmpl)
    else:
        # 引数がない場合は対話モード
        interactive_mode()
