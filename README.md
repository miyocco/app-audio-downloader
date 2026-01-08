# Radiko Audio Downloader

## 概要
RadikoのタイムフリーURLから音声ファイルをダウンロードするCLIツールです。
内部エンジンとして `yt-dlp` とそのプラグイン `yt-dlp-rajiko` を使用しており、安定したダウンロードが可能です。

## 必要要件
- Python 3.x
- ffmpeg (パスが通っていること)

## セットアップ
```bash
pip install -r requirements.txt
```

## 使い方



### 対話モード（推奨）

引数なしで実行すると、URLの入力を求められます。複数のURLをまとめて入力できます。



```bash

python3 src/main.py

```



実行例:

```text

RadikoのURLを入力してください。

（複数ある場合は改行して入力してください。入力完了時は何も入力せずにEnterを押してください）

> https://radiko.jp/#!/ts/LFR/20260102010000

> https://radiko.jp/#!/ts/BAYFM78/20251229210000

> 

Edgeブラウザのログイン情報（クッキー）を使用しますか？ (y/n) [n]: y



2 件のダウンロードを開始します...

```



### コマンドライン引数（従来の方法）

```bash

python src/main.py <URL> [output_filename]

```
