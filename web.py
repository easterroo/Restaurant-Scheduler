from datetime import datetime, timedelta
from flask import Flask, render_template, request

from app.database import create_tables
from app.weeks import get_week_range
from app.shifts import list_shifts, shift_hours, TIME_FORMAT
from app.scheduling import weekly_summary

web = Flask(__name__)
create_tables()


# Turns a datetime into a friendly time like "4:00 PM"
def fmt_time(dt):
    return dt.strftime("%I:%M %p").lstrip("0")


@web.route("/")
def week_view():
    # Optional ?day=2026-11-20 in the URL; blank means today
    day = request.args.get("day") or None
    week_start, week_end = get_week_range(day)

    monday = datetime.strptime(week_start, TIME_FORMAT)
    sunday = monday + timedelta(days=6)
    prev_day = (monday - timedelta(days=7)).strftime("%Y-%m-%d")
    next_day = (monday + timedelta(days=7)).strftime("%Y-%m-%d")

    shifts = []
    for shift_id, start, end, shift_type, emp_id, name, notes in list_shifts(week_start, week_end):
        start_dt = datetime.strptime(start, TIME_FORMAT)
        end_dt = datetime.strptime(end, TIME_FORMAT)
        shifts.append({
            "id": shift_id,
            "day": start_dt.strftime("%a %b %d"),
            "time": f"{fmt_time(start_dt)} - {fmt_time(end_dt)}",
            "hours": shift_hours(start, end),
            "server": name,            # None means the shift is open
            "type": shift_type or "",
            "notes": notes or "",
        })

    hours = [
        {"name": name, "hours": total}
        for emp_id, name, total in weekly_summary(week_start, week_end)
    ]

    return render_template(
        "week.html",
        title=f"{monday.strftime('%b %d')} to {sunday.strftime('%b %d, %Y')}",
        prev_day=prev_day,
        next_day=next_day,
        shifts=shifts,
        hours=hours,
        open_count=sum(1 for s in shifts if s["server"] is None),
    )


if __name__ == "__main__":
    web.run(debug=True, port=5001)