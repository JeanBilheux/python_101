from datetime import date
from calendar import monthcalendar


class Weekday:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def weekdays_in_month(year, month, weekday):
    """Return list of all 4/5 dates with given weekday and year/month."""
    return [
        date(year, month, week[weekday])
        for week in monthcalendar(year, month)
        if week[weekday] != 0
    ]


def meetup_date(year, month, *, nth=4, weekday=Weekday.THURSDAY):
    """Return date of the nth weekday of the given month."""
    return weekdays_in_month(year, month, weekday)[nth-1 if nth > 0 else nth]
