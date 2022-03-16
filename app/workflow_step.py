import datetime
import pytz
from typing import Optional, Union
from urllib.parse import quote

from slack_bolt import Ack, App
from slack_bolt.workflows.step import WorkflowStep, Configure, Update, Complete, Fail
from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError
from app.holidays import fetch_public_holiday, Holiday


# Keys
input_channel_ids = "channel_ids"
input_days_in_advance = "days_in_advance"


def edit(ack: Ack, step: dict, configure: Configure):
    ack()
    inputs = step.get("inputs")
    blocks = [
        {
            "type": "section",
            "block_id": "intro-section",
            "text": {
                "type": "plain_text",
                "text": "チャンネルに祝日を通知するための設定をしましょう :raised_hands:",
            },
        },
    ]
    channels_block = {
        "type": "input",
        "block_id": input_channel_ids,
        "label": {"type": "plain_text", "text": "通知したいチャンネル"},
        "element": {
            "type": "multi_channels_select",
            "placeholder": {"type": "plain_text", "text": "複数選択可能"},
            "action_id": "_",
        },
    }

    if input_channel_ids in inputs:
        value = inputs.get(input_channel_ids).get("value")
        if value is not None:
            channels_block["element"]["initial_channels"] = value.split(",")
    blocks.append(channels_block)

    days_in_advance_block_options = [
        {"text": {"type": "plain_text", "text": "当日"}, "value": "0"},
        {"text": {"type": "plain_text", "text": "1 日前"}, "value": "1"},
        {"text": {"type": "plain_text", "text": "2 日前"}, "value": "2"},
        {"text": {"type": "plain_text", "text": "3 日前"}, "value": "3"},
        {"text": {"type": "plain_text", "text": "4 日前"}, "value": "4"},
        {"text": {"type": "plain_text", "text": "5 日前"}, "value": "5"},
        {"text": {"type": "plain_text", "text": "6 日前"}, "value": "6"},
        {"text": {"type": "plain_text", "text": "7 日前"}, "value": "7"},
    ]
    days_in_advance_block = {
        "type": "input",
        "block_id": input_days_in_advance,
        "label": {"type": "plain_text", "text": "事前通知"},
        "element": {
            "type": "radio_buttons",
            "action_id": "_",
            "options": days_in_advance_block_options,
        },
    }
    if input_days_in_advance in inputs:
        value = inputs.get(input_days_in_advance).get("value")
        option = next(
            (o for o in days_in_advance_block_options if o.get("value") == value),
            None,
        )
        if option is not None:
            days_in_advance_block["element"]["initial_option"] = option
    blocks.append(days_in_advance_block)
    configure(blocks=blocks)


def save(ack: Ack, view: dict, update: Update):
    state_values = view["state"]["values"]
    channels = _extract(state_values, input_channel_ids, "selected_channels")
    days_in_advance = _extract(state_values, input_days_in_advance, "selected_option")
    update(
        inputs={
            input_channel_ids: {"value": ",".join(channels)},
            input_days_in_advance: {"value": days_in_advance},
        },
        outputs=[
            {
                "name": channel_id,
                "type": "text",
                "label": "Posted message timestamp",
            }
            for channel_id in channels
        ],
    )
    ack()


def enable_workflow_step(app: App, kenall_api_token: str):
    def execute(step: dict, client: WebClient, complete: Complete, fail: Fail):
        inputs = step.get("inputs", {})
        holiday: Optional[Holiday] = None
        try:
            days = int(inputs.get(input_days_in_advance).get("value"))
            now = datetime.datetime.now(pytz.timezone("Asia/Tokyo")).date()
            target_date = now + datetime.timedelta(days=days)
            holiday = fetch_public_holiday(kenall_api_token, target_date)
        except Exception as err:
            fail(error={"message": f"Notification failed ({err})"})
            return
        if holiday is not None:
            try:
                outputs = {}
                date = f"{target_date.year} 年 {target_date.month} 月 {target_date.day} 日"
                wikipedia_url = f"https://ja.wikipedia.org/wiki/{quote(holiday.title)}"
                message = f"{date}は「<{wikipedia_url}|{holiday.title}>」で祝日ですよー :wave:"
                for channel in inputs.get(input_channel_ids).get("value").split(","):
                    response = client.chat_postMessage(
                        channel=channel,
                        text=message,
                    )
                    outputs[channel] = response.get("message").get("ts")
                complete(outputs=outputs)
            except SlackClientError as err:
                fail(error={"message": f"Notification failed ({err})"})

    app.step(
        WorkflowStep(
            callback_id="japan-holiday-notification",
            edit=edit,
            save=save,
            execute=execute,
        )
    )


def _extract(
    state_values: dict, key: str, attribute: str
) -> Optional[Union[str, list]]:
    v = state_values[key].get("_", {})
    if v is not None and v.get(attribute) is not None:
        attribute_value = v.get(attribute)
        if isinstance(attribute_value, (list, str)):
            return attribute_value
        return attribute_value.get("value")
    return None
