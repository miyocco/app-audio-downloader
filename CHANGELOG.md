# app-audio-downloader - 変更履歴

このファイルは、プロジェクトの重要な変更をすべて記録します。

形式は [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づいており、
このプロジェクトは [セマンティック バージョニング](https://semver.org/lang/ja/) に 準拠しています。

---

## [Unreleased]

### 追加
- 対話モードによる複数URLの一括ダウンロード機能
- Edgeブラウザのクッキーを利用したプレミアム会員限定コンテンツのダウンロード機能
- ドキュメント (`ARCHITECTURE.md`, `TODO.md`) の詳細化

### 変更
- エントリーポイントを `src/main.py` から `download.py` に変更
- ドキュメントのフォーマットをプロジェクト標準 (`app-auto-monitor` 準拠) に統一

### 削除
- `src` ディレクトリ（ルートへの移動に伴い削除）

---

## [0.1.0] - 2026-01-08

### 追加
- プロジェクト初期化
- `yt-dlp` および `yt-dlp-rajiko` を使用したダウンロード機能
- CLIツールの基本実装