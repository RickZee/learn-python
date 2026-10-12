from datetime import datetime
from zoneinfo import ZoneInfo


def utc_now_zone():
    return ZoneInfo("UTC")


def ny_time(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=ZoneInfo("America/New_York"))


def utc_hour_from_ny(year: int, month: int, day: int, hour: int, minute: int) -> int:
    return ny_time(year, month, day, hour, minute).astimezone(ZoneInfo("UTC")).hour
