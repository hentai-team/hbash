# HBash - 高度なターミナルエミュレーター

![HBash ロゴ](https://github.com/hentai-team/hbash/blob/main/assets/hbash-splash-jp.png?raw=true)

## 概要
HBashは、Pythonで書かれた機能豊富なターミナルエミュレーターで、高度な機能性、ユーザー管理、カスタマイズオプションを備えた最新のコマンドラインインターフェースを提供します。

## 機能

### 主要機能
- ユーザー認証と管理
- 多言語対応（英語、ロシア語）
- カラフルでカスタマイズ可能なインターフェース
- コマンド履歴
- エイリアスのサポート
- Cronライクなタスクスケジューリング

### ファイル操作
- 基本的なファイル操作（cp、mv、rm、mkdir、touch）
- ファイル内容の表示と操作（cat、head、tail）
- ファイルの検索と比較（find、grep、diff）
- アーカイブ管理（zip、unzip、tar、gzip）

### システムツール
- システム監視（ps、top、df、free）
- ネットワークユーティリティ（ping、ifconfig、ssh、scp）
- プロセス管理
- リソース監視

### 追加ツール
- シンタックスハイライト付きテキストエディタ
- ToDoリストマネージャー
- ノート取りシステム
- カレンダー
- 天気情報
- タイマーとストップウォッチ

## インストール

1. リポジトリをクローン：
```bash
git clone https://github.com/yourusername/hterm.git
```

2. 必要な依存関係をインストール：
```bash
pip install -r requirements.txt
```

## 使用方法

### HBashの起動
```bash
python hbash.py
```

### デフォルトログイン
デフォルトのrootアカウントの認証情報は以下の通りです：
```bash
ユーザー名: root
パスワード: root
```
これは実際には試験的に追加された機能であり、新しいバージョンでは削除される予定です。

### 基本コマンド
- `help` - 利用可能なコマンドを表示
- `quit` - HTermを終了
- `clear` - 画面をクリア
- `ver` - バージョン情報を表示

### ユーザー管理
- `login` - システムにログイン
- `logout` - 現在のユーザーをログアウト
- `adduser` - 新規ユーザーを追加（root専用）
- `deluser` - ユーザーを削除（root専用）

### 追加ドキュメント

各言語のコマンドの詳細なドキュメントはdocsフォルダにあります：
[英語](https://github.com/hentai-team/hbash/blob/main/docs/commands-en.md) | [ロシア語](https://github.com/hentai-team/hbash/blob/main/docs/commands-ru.md) | [日本語](https://github.com/hentai-team/hbash/blob/main/docs/commands-jp.md) | [中国語](https://github.com/hentai-team/hbash/blob/main/docs/commands-ch.md)

## 設定
- デフォルト設定は`config.json`に保存
- 言語設定は`localization`ディレクトリに
- ユーザーデータは`users.json`に

## カスタマイズ
- カスタムカラースキーム
- 設定可能なプロンプト
- 頻繁に使用するコマンドのエイリアス
- ユーザーごとの個人設定

## 要件
- Python 3.7以上
- requirements.txtに記載された必要パッケージ

## 貢献
貢献は歓迎します！プルリクエストをお気軽にご提出ください。

## ライセンス
このプロジェクトはMITライセンスの下で提供されています - 詳細はLICENSEファイルをご覧ください。

## サポート
サポートが必要な場合は、GitHubリポジトリでイシューを開いてください。

