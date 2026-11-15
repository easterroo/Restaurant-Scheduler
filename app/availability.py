from app.database import get_connection
from datetime import datetime

# Returns employee's weekly availability
def get_availability(employee_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT day_of_week, start_time, end_time FROM availability WHERE employee_id = ? ORDER BY day_of_week",
        (employee_id,),
    ).fetchall()
    conn.close()
    return rows

# Deleted and re-inserts updated availability when changed
def set_availability(employee_id, day_of_week, start_time, end_time):
    conn = get_connection()
    conn.execute(
        "DELETE FROM availability WHERE employee_id = ? AND day_of_week = ?",
        (employee_id, day_of_week),
    )
    conn.execute(
        "INSERT INTO availability (employee_id, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)",
        (employee_id, day_of_week, start_time, end_time),
    )
    conn.commit()
    conn.close()

# Returns True if the shift fits inside the employee's availability that day
def is_available(employee_id, start_time, end_time):
    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    day = start.weekday()  # 0 = Monday ... 6 = Sunday

    conn = get_connection()
    row = conn.execute(
        "SELECT start_time, end_time FROM availability WHERE employee_id = ? AND day_of_week = ?",
        (employee_id, day),
    ).fetchone()
    conn.close()

    if row is None:
        return False  # no row for that day means not available

    window_start, window_end = row
    shift_start = start.strftime("%H:%M")
    # A shift that ends after midnight is treated as ending at 23:59
    shift_end = end.strftime("%H:%M") if end.date() == start.date() else "23:59"

    return window_start <= shift_start and shift_end <= window_end

# Marks employee as unavailable for that day
def clear_availability(employee_id, day_of_week):
    conn = get_connection()
    conn.execute(
        "DELETE FROM availability WHERE employee_id = ? AND day_of_week = ?",
        (employee_id, day_of_week),
    )
    conn.commit()
    conn.close()