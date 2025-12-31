# Chat-ZPT

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/docker-supported-2496ED)

**Zundamon Prompt-tuned Transformer**

Discordのボイスチャット(VC)において、「ずんだもん」とお話しができるBotです。
Google Geminiによる対話生成と、VOICEVOXによる音声読み上げ機能に対応しています。  
> **Note**  
> ピンと来た方もいるかもしれませんが、Pre-trained Transformerではありません。  
> 名前は某AIへのリスペクトとパロディです。中身はGeminiが頑張っています。

##  機能

* **VC読み上げ**: テキストチャットの内容をずんだもんの声で読み上げます。
* **AI対話**: Gemini APIを利用し、メンションで話しかけると音声付きで返答します。
* **ハイブリッド構成**: Docker環境とローカル環境の両方に対応しています。

##  導入方法

OSは Windows / macOS / Linux いずれでも動作します。
Dockerを使用した起動を推奨していますが、Dockerを使用しない場合の手順も後述します。

### 事前準備 (共通)

1.  このリポジトリをクローンします。
    ```bash
    git clone https://github.com/yoimya77/Chat-ZPT.git
    cd Chat-ZPT
    ```
2.  `.env` ファイルを開き、APIキーを設定してください。
    ```text
    DISCORD_TOKEN = "ENTER_YOUR_TOKEN"
    GEMINI_API_KEY = ENTER_YOUR_API_KEY
    ```

---

### パターンA：Dockerを使用する場合 (推奨)

Docker Desktop等がインストールされている環境であれば、コマンド一つで環境構築が完了します。

1.  ディレクトリ直下で以下のコマンドを実行します。
    ```bash
    docker compose up --build
    ```

2.  ビルドが完了すると自動的にサーバーが立ち上がりますが、このままだとログが見えないので一旦終了してください。
3.  以下のコマンドを実行します。
    ```bash
    docker compose run --rm app
    ```
    ログに `Logged In.` と表示されれば起動成功です。

> **Note**  
> 終了する場合は `Ctrl + C` を押してください。

---

### パターンB：Dockerを使用しない場合

Dockerを使わず、PythonとVOICEVOX Engineを手動で動かす方法です。

#### 1. VOICEVOX Engine の起動
Bot本体とは別に、音声合成エンジンを起動しておく必要があります。

1.  [VOICEVOX EngineのReleases](https://github.com/VOICEVOX/voicevox_engine/releases) から、お使いのOSに合ったバージョンをダウンロード・解凍してください。
2.  ターミナルで解凍したフォルダへ移動し、実行します。

    **macOSの例:**
    ```bash
    cd Downloads/macos-arm64
    ./run
    ```
    

#### 2. ソースコードの修正
ローカル環境で動かす場合、接続先設定の変更が必要です。
`voicevox.py` をエディタで開き、以下のように修正してください。

```python
# voicevox.py

# 修正前
host = "voicevox_engine" 

# 修正後
host = "127.0.0.1"
```

※ `requests.post` のURL部分にある `http://voicevox_engine:50021/...` を `http://127.0.0.1:50021/...` に書き換えてください。

#### 3. 依存ライブラリのインストールと起動

Python (3.10以上推奨) の仮想環境を作成し、ライブラリをインストールします。

```bash
# 仮想環境の作成と有効化 (例)
python -m venv venv
source venv/bin/activate  # Windowsなら .\venv\Scripts\activate

# ライブラリインストール
pip install -r requirements.txt

# Botの起動
python3 Chat-ZPT.py
```

`Logged In` と表示されたら起動成功です。

---

##  使い方

### 1. `!join`

ボイスチャンネルに参加した状態でコマンドを打つと、Botが入室します。
入室中にチャットを送信すると、ずんだもんの声で読み上げを行います。

### 2. `@Chat-ZPT [質問]`

Botにメンションを飛ばして質問すると、ずんだもん（Gemini）が返答を生成し、声に出して回答してくれます。

* 例: `@Chat-ZPT 今日の晩御飯のおすすめは？`

### 3. `!leave`

Botを退室させます。
※ ユーザーが全員いなくなると自動で退室する機能も搭載しています。

---

##  開発背景など

本Botの制作過程や、技術的な解説（Docker構成、Gemini連携など）をZennにて公開予定です。
これからBotを作りたい方の参考になれば幸いです。

* [Zennの記事はこちら (26年1月中に公開予定)](https://zenn.dev/)

---

## Credits / 謝辞

Bot制作にあたって使用させていただいた素晴らしいライブラリを紹介します。

* **Libraries:**
    * [discord.py](https://github.com/Rapptz/discord.py)
    * [requests](https://github.com/psf/requests)
    * [google-genai](https://github.com/googleapis/python-genai)


* **Voice Synthesis Engine:**
    * [VOICEVOX Engine](https://github.com/VOICEVOX/voicevox_engine) (LGPL v3)  
    Special thanks to Hiroshiba and all contributors.


* **Character:**
    * ずんだもん (SSS合同会社)