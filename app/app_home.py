from slack_bolt import App, BoltContext
from slack_sdk import WebClient


def enable_app_home_event_handler(app: App):
    @app.event("app_home_opened")
    def handle_app_home_opened_events(context: BoltContext, client: WebClient):
        client.views_publish(
            user_id=context.user_id,
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "日本の祝日をお伝えするアプリです :jp:"},
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "任意のチャンネルでこのアプリのボットをメンションすると次の祝日を教えてくれます。",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "ワークフロービルダーで定期実行のワークフローを作って、このアプリが提供しているカスタムのステップを追加してみてください。"
                            "休日が近づいたときにチャンネルにメッセージを投稿してくれます。",
                        },
                    },
                ],
            },
        )
