# app-audio-downloader

Radikoのタイムフリー音源をダウンロードするためのCLIツール。

## 概要

このツールは、RadikoのタイムフリーURLを入力として受け取り、`yt-dlp` と `yt-dlp-rajiko` を使用して高品質な音声ファイル（m4a）をダウンロードします。

### 主な機能

- 📥 **簡単ダウンロード**: URLを入力するだけで自動ダウンロード
- 💬 **対話モード**: 複数のURLをまとめて入力・処理可能
- 🔐 **プレミアム対応**: Edgeブラウザのクッキーを利用してエリアフリー/タイムフリー30もダウンロード可能
- 🛠 **高信頼性**: `yt-dlp` エンジンを採用し、安定したダウンロードを実現

## セットアップ

### 1. 依存パッケージのインストール

```bash
cd /Users/miyoshi-koichi/cursor/miyocco/app-audio-downloader
pip3 install -r requirements.txt
```

### 2. 環境変数の設定（推奨）

Radikoプレミアム会員の方は、プロジェクトルートに `.env` ファイルを作成し、ログイン情報を設定することで、毎回入力する手間を省けます。

```bash
cp .env.example .env
nano .env  # またはお好みのエディタで編集
```

`.env` の内容:
```ini
RADIKO_MAIL=your_email@example.com
RADIKO_PASSWORD=your_password
```

### 3. ffmpegの確認

`ffmpeg` がインストールされている必要があります。

```bash
ffmpeg -version
```

## 使い方

### 対話モード（推奨）

スクリプトを実行すると、URLの入力を求められます。複数のURLをまとめて入力できます。

```bash
cd cursor/miyocco/app-audio-downloader
python3 download.py
```

実行例:
```text
保存先: /Users/miyoshi-koichi/Desktop
RadikoのURLを入力してください。
（複数ある場合は改行して入力してください。入力完了時は何も入力せずにEnterを押してください）
> https://radiko.jp/#!/ts/LFR/20260102010000
> https://radiko.jp/#!/ts/BAYFM78/20251229210000
> 
Edgeブラウザのログイン情報（クッキー）を使用しますか？ (y/n) [n]: y

2 件のダウンロードを開始します...
```

**保存先**: デフォルトで **デスクトップ** (`~/Desktop`) に保存されます。

### コマンドライン引数（単一ダウンロード）

```bash
cd cursor/miyocco/app-audio-downloader
python3 download.py <URL> [output_filename]
```

## 開発情報

- **言語**: Python 3.x
- **コアエンジン**: yt-dlp + yt-dlp-rajiko
- **依存ツール**: ffmpeg

詳細は以下のドキュメントを参照:

- [ARCHITECTURE.md](ARCHITECTURE.md): 技術設計書
- [TODO.md](TODO.md): 開発タスク
- [CHANGELOG.md](CHANGELOG.md): 変更履歴

## ライセンス

個人用プロジェクト