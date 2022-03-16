import logging
from typing import Optional

import requests
import datetime
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class Holiday:
    title: str
    date: str
    day_of_week: str
    day_of_week_text: str


def fetch_public_holiday(token: str, target_date: datetime.date) -> Optional[Holiday]:
    response = requests.get(
        url="https://api.kenall.jp/v1/holidays",
        headers={"Authorization": f"Token {token}"},
        params={"year": target_date.year},
    )
    target_date_str = str(target_date)
    response_body = response.json()
    logger.debug(response_body)
    for holiday in response_body.get("data"):
        if holiday.get("date") == target_date_str:
            return Holiday(**holiday)
    return None


def fetch_next_public_holiday(
    token: str, target_date: datetime.date
) -> Optional[Holiday]:
    response = requests.get(
        url="https://api.kenall.jp/v1/holidays",
        headers={"Authorization": f"Token {token}"},
        params={"year": target_date.year},
    )
    response_body = response.json()
    logger.debug(response_body)
    for holiday in response_body.get("data"):
        if datetime.date.fromisoformat(holiday.get("date")) >= target_date:
            return Holiday(**holiday)
    next_new_year_day = datetime.date(target_date.year + 1, 1, 1)
    return fetch_next_public_holiday(next_new_year_day)
