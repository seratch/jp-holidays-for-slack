## 日本の祝日 API!!!

[ケンオール](https://kenall.jp/)というサービスから「日本の祝日 API」という新しい Web API が公開されました。以下の通り、Twitter 上でも大変話題になっていますね！

https://twitter.com/kenalljp/status/1503884558105989120

この API の詳細についてはケンオールが公開している以下の情報をご参照ください。

* https://blog.kenall.jp/entry/japan-holiday-api-release
* https://kenall.jp/features/holidays

## Slack と連携させてみよう

この API を使った Slack アプリをすきま時間でサクッとつくってみました。シンプルですが、なかなか実用的なアプリになっているのではないか？と思っています。

以下の GitHub リポジトリでコードを公開しています。どうぞ自由にカスタマイズしてご利用ください！

https://github.com/seratch/jp-holidays-for-slack

それでは、アプリの紹介をしていきます。

## アプリの概要と使い方

改めて、この記事で紹介するアプリは、ケンオールが提供する「[日本の祝日 API](https://kenall.jp/docs/API/holidays/)」を使って Slack チャンネル内で祝日の情報を共有してくれるアプリです。

以下の通り、二つの使い方があります。

* ワークフロービルダーで定期実行してチャンネルに事前通知
* ボットをメンションして次の祝日を教えてもらう

それでは、順に説明していきます。

### ワークフロービルダーで定期実行してチャンネルに事前通知

以下のスクリーンショットのようなとてもシンプルなワークフローをつくってください。export したものが [jp-holidays-workflow.json](https://github.com/seratch/jp-holidays-for-slack/blob/main/jp-holidays-workflow.json) として、先ほど共有した GitHub リポジトリに置いてありますので、それを import しても OK です。

<img width="600" src="https://user-images.githubusercontent.com/19658/158530327-623422e0-f40f-49d7-860d-046fa656f351.png">

ステップの設定は以下のように通知先のチャンネル（現在の実装ではパブリックチャンネルのみ、複数指定可能）を指定した上で、何日前に知りたいかを指定します。

例えば 3/16 の時点で 3/21 の春分の日を通知してほしい場合は 5 日前に設定します。

<img width="600" src="https://user-images.githubusercontent.com/19658/158530312-0c2705ae-f614-4a94-a93c-617b291cc05f.png">

こうすることで、以下の様な通知が指定したチャンネルに届きます。こだわりポイント（？）は Wikipedia の URL をリンクしているところですね。

<img width="600" src="https://user-images.githubusercontent.com/19658/158533554-e137712a-3713-4811-b1fd-5e0891823245.png">

もしこの通知タイミングなどの設定をチャンネルごとに分けたい場合、ワークフローを複数作ってください。このアプリを複数のワークフローから呼び出すことも全く問題ありません。

### ボットをメンションして次の祝日を知る

「最近、祝日がない気がするなぁ・・次の連休はいつだろう・・」

そんな気持ちになったときは、このアプリのボットをメンションしてみてください。

次に来る祝日を教えてくれますので、気持ちが明るくなるかもしれません（逆かも？）。

<img width="600" src="https://user-images.githubusercontent.com/19658/158530366-7114289d-44ff-454e-bbd5-400a6da99ddf.png">

ということで、地味に便利なアプリではないかと思ってたりするのですが、いかがでしょうか？

## アプリの動かし方

どういうアプリかわかったところで、次は GitHub にあるコードを動かす手順について紹介していきます。

このアプリは [Bolt for Python](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started) で実装されたシンプルな Python アプリケーションです。

Slack のサーバーに[ソケットモード](https://qiita.com/seratch/items/1a460c08c3e245b56441)という WebSocket のコネクション経由で接続します。このアプリに限らないソケットモードの一般的なはじめ方については、以下の記事も参考にしてみてください。

https://qiita.com/seratch/items/1a460c08c3e245b56441

まずは手元で動かしてみましょう。

### ケンオールの API トークンの取得

まずはじめに[ケンオール](https://kenall.jp/)の API トークンを取得して環境変数に設定してください。

```bash
# https://kenall.jp/home で入手してください
export KENALL_API_TOKEN=
```

### Slack アプリ設定 & ワークスペースにインストール

次に、新しい Slack アプリの設定を https://api.slack.com/apps から作成してください。アプリをつくるときに、GitHub リポジトリにある [app-manifest.yml](https://github.com/seratch/jp-holidays-for-slack/blob/main/app-manifest.yml) の内容を流用すると簡単に設定することができます。

アプリ設定が作られたら **Settings** > **Basic Information** > **App-Level Tokens** のセクションから `connections:write` のスコープが付与されたトークンを作成してください。それを `SLACK_APP_TOKEN` として環境変数に設定します。

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

その上で Python のプロジェクトを設定します。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

か、もし [Poetry](https://python-poetry.org/) に馴染みがあるなら

```bash
poetry shell && poetry update
```

でプロジェクトをセットアップした上で、以下のコマンドでアプリを起動してみてください。特にエラーメッセージが出なければ大丈夫でしょう。

```bash
python app.py
```

### ワークスペース内で設定

この状態であればワークフロービルダーの設定画面でステップを選択できる様になっているはずです。
「使い方」のパートを参考に設定してみてください。

ボットをメンションする使い方をしたい場合は、ボットをチャンネルに招待して話しかけてみてください。

## デプロイして運用するには？

Heroku などの環境で動かすのが簡単かもしれません。 デプロイボタンを置いておきますね。
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/seratch/jp-holidays-for-slack/tree/main)
なお、ソケットモードはただ WebSocket のクライアントプロセスが起動するだけなので、Heroku で動かす場合は Procfile を web ではなく worker で設定するのがよいかと思います。

また GitHub リポジトリに Dockerfile も置いておきますので、コンテナサービスで動かす場合は、そちらを利用されてもよいかと思います。

## 最後に

ということで、ケンオールの新しい API である「日本の祝日 API」を使った Slack アプリをご紹介しました。

そういえば、郵便番号の API の方も Slack 連携の実装例をご紹介していました（Twitter 上だけでの告知でしたが）。もしご興味あれば、こちらもぜひご覧ください！

https://twitter.com/seratch_ja/status/1361213198498598914

それでは :wave:
