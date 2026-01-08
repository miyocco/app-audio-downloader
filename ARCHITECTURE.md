# Architecture

## 概要
本ツールは、Radikoのタイムフリー音源をダウンロードするためのラッパーツールです。
複雑な認証プロセスやストリーム処理を自前で実装する代わりに、信頼性の高いOSSである `yt-dlp` とそのRadiko用プラグイン `yt-dlp-rajiko` を利用しています。

## コンポーネント

- **CLI Entrypoint (`src/main.py`)**: 
  - ユーザーからの入力を受け付けます。
  - `yt_dlp` ライブラリを呼び出します。

- **Engine (`yt-dlp` + `yt-dlp-rajiko`)**:
  - **yt-dlp**: 動画/音声ダウンロードのコアフレームワーク。
  - **yt-dlp-rajiko**: Radiko固有の認証（auth1/auth2）、プレイリスト取得、エリア判定などを処理するプラグイン。

## フロー
1. ユーザーが `src/main.py` を実行。
2. Pythonスクリプトが `yt_dlp.YoutubeDL` インスタンスを作成。
3. `yt-dlp` が `yt-dlp-rajiko` プラグインをロード。
4. RadikoのAPIと通信し、ストリームURL (m3u8) を特定。
5. 音声データをダウンロードし、指定されたフォーマット（m4a等）で保存。