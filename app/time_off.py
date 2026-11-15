from app.database import get_connection


# Records time off. Use "YYYY-MM-DD HH:MM" for both values.
# Full day off: 00:00 on the day to 00:00 the day after the last day off.
def add_time_off(employee_id, start_time, end_time):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO time_off (employee_id, start_time, end_time) VALUES (?, ?, ?)",
        (employee_id, start_time, end_time),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


# Lists an employee's time off that overlaps a date range
def list_time_off(employee_id, range_start, range_end):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, start_time, end_time FROM time_off
        WHERE employee_id = ? AND start_time < ? AND end_time > ?
        ORDER BY start_time
        """,
        (employee_id, range_end, range_start),
    ).fetchall()
    conn.close()
    return rows


# Returns True if the given window overlaps any of the employee's time off
def has_time_off(employee_id, start_time, end_time):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT 1 FROM time_off
        WHERE employee_id = ? AND start_time < ? AND end_time > ?
        LIMIT 1
        """,
        (employee_id, end_time, start_time),
    ).fetchone()
    conn.close()
    return row is not None

# Deletes time off
def delete_time_off(time_off_id):
    conn = get_connection()
    conn.execute(
        "DELETE FROM time_off WHERE id = ?",
        (time_off_id,),
    )
    conn.commit()
    conn.close()
