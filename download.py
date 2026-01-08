import sys
import yt_dlp
import os

def download_radiko(url, output_template=None, use_browser_cookies=False):
    """
    Downloads Radiko audio using yt-dlp.
    
    Args:
        url (str): The Radiko URL.
        output_template (str, optional): Output filename template. 
                                         Defaults to '%(title)s [%(id)s].%(ext)s'.
        use_browser_cookies (bool): Whether to use cookies from the browser (Edge).
    """
    ydl_opts = {
        'outtmpl': output_template if output_template else '%(title)s [%(id)s].%(ext)s',
        'format': 'bestaudio/best',
    }
    
    if use_browser_cookies:
        # Edgeからクッキーを読み込む設定
        ydl_opts['cookiesfrombrowser'] = ('edge', None, None, None)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        # 対話モードで1つ失敗しても他を続行できるようにsys.exitは削除または制御
        pass

def interactive_mode():
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

    print(f"\n{len(urls)} 件のダウンロードを開始します...\n")
    
    for url in urls:
        print(f"Processing: {url}")
        download_radiko(url, use_browser_cookies=use_cookies)
        print("-" * 40)

if __name__ == "__main__":
    # 引数がある場合は従来通り処理
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        out_tmpl = sys.argv[2] if len(sys.argv) > 2 else None
        print(f"Downloading from: {target_url}")
        download_radiko(target_url, out_tmpl)
    else:
        # 引数がない場合は対話モード
        interactive_mode()
