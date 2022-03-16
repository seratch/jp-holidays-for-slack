# Notifying National Holiday in Japan to Slack Channels

この Slack アプリは、[ケンオールが提供する日本の祝日 API](https://kenall.jp/docs/API/holidays/) を使って Slack 内で祝日の情報をポストします。

## 使い方

二つの使い方があります。

* ワークフロービルダーで定期実行して祝日を通知
* ボットをメンションして次の祝日を教えてもらう

### ワークフロービルダー

以下のスクリーンショットのようなとてもシンプルなワークフローをつくってください。export したものが jp-holidays-workflow.json としてこのリポジトリに置いてありますので、それを import しても OK です。

<img width="600" src="https://user-images.githubusercontent.com/19658/158530327-623422e0-f40f-49d7-860d-046fa656f351.png">

ステップの設定は以下のように通知先のチャンネル（現在の実装ではパブリックチャンネルのみ、複数指定可能）を指定した上で、何日前に知りたいかを指定します。例えば 3/16 の時点で 3/21 の春分の日を通知してほしい場合は 5 日前に設定します。

<img width="600" src="https://user-images.githubusercontent.com/19658/158530312-0c2705ae-f614-4a94-a93c-617b291cc05f.png">

もし設定を分けたい場合はワークフローを複数作ってください。このアプリを複数のワークフローで利用することも全く問題ありません。

### ボットをメンション

「最近、祝日がない気がするなぁ・・次の連休はいつだろう・・」という気持ちになったときは、このアプリのボットをメンションしてみてください（チャンネルに招待しておく必要があります）。次に来る祝日を教えてくれますので、気持ちが明るくなるかもしれません（逆かも）。

<img width="600" src="https://user-images.githubusercontent.com/19658/158530366-7114289d-44ff-454e-bbd5-400a6da99ddf.png">

## 動かし方

### トークンの取得

まずはじめに[ケンオール](https://kenall.jp/)の API トークンを取得して環境変数に設定してください。

```bash
# https://kenall.jp/home で入手してください
export KENALL_API_TOKEN=
```

次に新しい Slack アプリの設定を https://api.slack.com/apps から作成してください。アプリをつくるときに、このリポジトリにある app-manifest.yml を利用すると簡単に設定することができます。

**Basic Information** > **App-Level Tokens** のセクションから `connections:write` のスコープをもったトークンを作成してください。それを `SLACK_APP_TOKEN` として環境変数に設定します。

```bash
# https://api.slack.com/apps の Basic Information で　App-Level Token を生成して入手してください
export SLACK_APP_TOKEN=xapp-
```

次にアプリを **Settings** > **Install App** からワークスペースにインストールして発行されたトークンを `SLACK_BOT_TOKEN` として設定してください。

```bash
# Slack ワークスペースにアプリをインストールして入手してください
export SLACK_BOT_TOKEN=xoxb-
```

### アプリの初期化と起動

その上で

```bash
poetry shell && poetry update
```
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```bash
python app.py
```

### ワークスペース内で設定

この状態であればワークフロービルダーの設定画面でステップを選択できる様になっているはずです。
「使い方」のパートを参考に設定してみてください。

ボットをメンションする使い方をしたい場合は、ボットをチャンネルに招待して話しかけてみてください。

## ライセンス

MIT ライセンスで公開します。利用する場合は自由にカスタマイズしてご利用ください。
