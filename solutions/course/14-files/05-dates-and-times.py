from datetime import datetime
from zoneinfo import ZoneInfo


def utc_now_zone():
    return ZoneInfo("UTC")


def ny_time(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=ZoneInfo("America/New_York"))


def utc_hour_from_ny(year: int, month: int, day: int, hour: int, minute: int) -> int:
    local = ny_time(year, month, day, hour, minute)
    utc = local.astimezone(ZoneInfo("UTC"))
    result = utc.hour
    return result


def same_clock() -> bool:
    naive = datetime(2024, 6, 1, 9, 0)
    aware = datetime(2024, 6, 1, 9, 0, tzinfo=ZoneInfo("UTC"))
    naive_utc = naive.replace(tzinfo=ZoneInfo("UTC"))
    return naive_utc == aware
