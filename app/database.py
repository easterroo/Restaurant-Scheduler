import sqlite3
from pathlib import Path

# Points to file scheduler.db
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "scheduler.db"

# Connects the program to the connection string
def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# If the tables don't exist, they will be created
def create_tables():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            notes TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS shift (
            id INTEGER PRIMARY KEY,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            type TEXT,
            employee_id INTEGER REFERENCES employee(id),
            notes TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL REFERENCES employee(id),
            day_of_week INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            notes TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS time_off (
            id INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL REFERENCES employee(id),
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database ready")