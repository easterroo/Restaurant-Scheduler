from app.database import get_connection

# Adds employee with name and optional notes
def add_employee(name, notes=None):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO employee (name, notes) VALUES (?, ?)",
        (name, notes),
    )
    new_id = cursor.lastrowid

    conn.executemany(
        "INSERT INTO availability (employee_id, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)",
        [(new_id, day, "00:00", "23:59") for day in range(7)],
    )

    conn.commit()
    conn.close()
    return new_id

# Returns a list of all employees, filtered by active or not
def list_employees(active_only=True):
    conn = get_connection()
    query = "SELECT id, name, active, notes FROM employee"
    if active_only:
        query += " WHERE active = 1"
    query += " ORDER BY name"
    rows = conn.execute(query).fetchall()
    conn.close()
    return rows

# Marks an employee as deactivated
def deactivate_employee(employee_id):
    conn = get_connection()
    conn.execute(
        "UPDATE employee SET active = 0 WHERE id = ?",
        (employee_id,),
    )
    conn.commit()
    conn.close()

# Deletes employee from database
def delete_employee(employee_id):
    conn = get_connection()
    conn.execute(
        "DELETE FROM employee WHERE employee_id = ?",
        (employee_id,),
    )
    conn.commit()
    conn.close()

# Fixes a name or edits notes for an employee
def update_employee(employee_id, name, notes=None):
    conn = get_connection()
    conn.execute(
        "UPDATE employee SET name = ?, notes = ? WHERE id = ?",
        (name, notes, employee_id),
    )
    conn.commit()
    conn.close()


# Brings a deactivated employee back
def reactivate_employee(employee_id):
    conn = get_connection()
    conn.execute(
        "UPDATE employee SET active = 1 WHERE id = ?",
        (employee_id,),
    )
    conn.commit()
    conn.close()