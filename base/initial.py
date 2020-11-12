from datetime import date, datetime


def datetime_today() -> datetime:
    return datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)


def date_today() -> date:
    return datetime.utcnow().date()
