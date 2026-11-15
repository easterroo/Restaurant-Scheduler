from app.database import create_tables
from app.employees import add_employee
from app.shifts import create_shift, assign_shift

create_tables()
a = add_employee("Person A")
b = add_employee("Person B")

s1 = create_shift("2026-11-20 16:00", "2026-11-20 21:00", "dinner")
s2 = create_shift("2026-11-20 17:00", "2026-11-20 22:00", "dinner")
s3 = create_shift("2026-11-21 12:00", "2026-11-21 20:00", "other", "long day")
assign_shift(s1, a)
assign_shift(s2, b)