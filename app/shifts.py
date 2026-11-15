from datetime import datetime
from app.database import get_connection

TIME_FORMAT = "%Y-%m-%d %H:%M"


def create_shift(start_time, end_time, shift_type=None, notes=None):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO shift (start_time, end_time, type, notes) VALUES (?, ?, ?, ?)",
        (start_time, end_time, shift_type, notes),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


# week_start is Monday 00:00, week_end is the next Monday 00:00
def list_shifts(week_start, week_end):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT shift.id, shift.start_time, shift.end_time, shift.type,
            shift.employee_id, employee.name, shift.notes
        FROM shift
        LEFT JOIN employee ON employee.id = shift.employee_id
        WHERE shift.start_time >= ? AND shift.start_time < ?
        ORDER BY shift.start_time
        """,
        (week_start, week_end),
    ).fetchall()
    conn.close()
    return rows


# Puts an employee on a shift
def assign_shift(shift_id, employee_id):
    conn = get_connection()
    conn.execute(
        "UPDATE shift SET employee_id = ? WHERE id = ?",
        (employee_id, shift_id),
    )
    conn.commit()
    conn.close()


# Makes a shift open again
def unassign_shift(shift_id):
    conn = get_connection()
    conn.execute(
        "UPDATE shift SET employee_id = NULL WHERE id = ?",
        (shift_id,),
    )
    conn.commit()
    conn.close()


# Changes a shift's times
def update_shift_times(shift_id, start_time, end_time):
    conn = get_connection()
    conn.execute(
        "UPDATE shift SET start_time = ?, end_time = ? WHERE id = ?",
        (start_time, end_time, shift_id),
    )
    conn.commit()
    conn.close()


# Length of a shift in hours, like 5.0 or 7.5
def shift_hours(start_time, end_time):
    start = datetime.strptime(start_time, TIME_FORMAT)
    end = datetime.strptime(end_time, TIME_FORMAT)
    return (end - start).total_seconds() / 3600


# Total hours an employee is scheduled for in one week
def weekly_hours(employee_id, week_start, week_end):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT start_time, end_time FROM shift
        WHERE employee_id = ? AND start_time >= ? AND start_time < ?
        """,
        (employee_id, week_start, week_end),
    ).fetchall()
    conn.close()
    return sum(shift_hours(start, end) for start, end in rows)

# Deletes shift
def delete_shift(shift_id):
    conn = get_connection()
    conn.execute(
        "DELETE FROM shift WHERE id = ?",
        (shift_id,),
    )
    conn.commit()
    conn.close()

# Lists shifts in a week that nobody is assigned to yet
def get_open_shifts(week_start, week_end):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, start_time, end_time, type, notes
        FROM shift
        WHERE employee_id IS NULL AND start_time >= ? AND start_time < ?
        ORDER BY start_time
        """,
        (week_start, week_end),
    ).fetchall()
    conn.close()
    return rows
