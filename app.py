import logging
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app.app_home import enable_app_home_event_handler
from app.app_mention import enable_app_mention_event_handler
from app.workflow_step import enable_workflow_step

logging.basicConfig(level=logging.DEBUG)

kenall_api_token = os.environ.get("KENALL_API_TOKEN")

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


enable_app_home_event_handler(app)
enable_app_mention_event_handler(app, kenall_api_token)
enable_workflow_step(app, kenall_api_token)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
