from datetime import datetime, date, timedelta

TIME_FORMAT = "%Y-%m-%d %H:%M"


# Takes any day ("YYYY-MM-DD", or leave blank for today) and returns
# that week's Monday 00:00 and the next Monday 00:00
def get_week_range(day=None):
    if day is None:
        day = date.today()
    elif isinstance(day, str):
        day = datetime.strptime(day, "%Y-%m-%d").date()
    elif isinstance(day, datetime):
        day = day.date()

    monday = day - timedelta(days=day.weekday())   # weekday(): 0 = Monday
    start = datetime.combine(monday, datetime.min.time())
    end = start + timedelta(days=7)
    return start.strftime(TIME_FORMAT), end.strftime(TIME_FORMAT)