import datetime
from logging import Logger
from urllib.parse import quote

from slack_bolt import App, Say
from slack_sdk.errors import SlackClientError
from app.holidays import fetch_next_public_holiday


def enable_app_mention_event_handler(app: App, kenall_api_token: str):
    @app.event("app_mention")
    def handle_app_mention_events(logger: Logger, say: Say):
        try:
            holiday = fetch_next_public_holiday(kenall_api_token, datetime.date.today())
            holiday_date = datetime.date.fromisoformat(holiday.date)
            date = f"{holiday_date.year} 年 {holiday_date.month} 月 {holiday_date.day} 日"
            wikipedia_url = f"https://ja.wikipedia.org/wiki/{quote(holiday.title)}"
            message = f"次の祝日は「<{wikipedia_url}|{holiday.title}>」（{date}）ですよー :wave:"
            say(text=message)
        except SlackClientError as err:
            logger.error(err)
