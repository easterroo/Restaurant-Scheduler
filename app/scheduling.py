from app.database import get_connection
from app.availability import is_available
from app.time_off import has_time_off
from app.shifts import assign_shift, weekly_hours
from app.employees import list_employees

# Returns True if the employee already has a shift overlapping this window.
# Pass ignore_shift_id so a shift doesn't conflict with itself.
def has_overlapping_shift(employee_id, start_time, end_time, ignore_shift_id=None):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT 1 FROM shift
        WHERE employee_id = ? AND start_time < ? AND end_time > ? AND id != ?
        LIMIT 1
        """,
        (employee_id, end_time, start_time, ignore_shift_id or -1),
    ).fetchone()
    conn.close()
    return row is not None


# Returns a list of reasons the employee can't work the shift.
# An empty list means they're good to go.
def get_conflicts(shift_id, employee_id):
    conn = get_connection()
    shift = conn.execute(
        "SELECT start_time, end_time FROM shift WHERE id = ?",
        (shift_id,),
    ).fetchone()
    conn.close()

    start_time, end_time = shift
    conflicts = []

    if not is_available(employee_id, start_time, end_time):
        conflicts.append("Not available at that time")
    if has_time_off(employee_id, start_time, end_time):
        conflicts.append("Has time off")
    if has_overlapping_shift(employee_id, start_time, end_time, shift_id):
        conflicts.append("Already working an overlapping shift")

    return conflicts


# Assigns the shift only if there are no conflicts.
# Returns the list of conflicts (empty means it worked).
# Pass force=True to assign anyway.
def try_assign(shift_id, employee_id, force=False):
    conflicts = get_conflicts(shift_id, employee_id)
    if conflicts and not force:
        return conflicts
    assign_shift(shift_id, employee_id)
    return []

# Every active employee with their scheduled hours for the week
def weekly_summary(week_start, week_end):
    summary = []
    for emp_id, name, active, notes in list_employees():
        hours = weekly_hours(emp_id, week_start, week_end)
        summary.append((emp_id, name, hours))
    return summary