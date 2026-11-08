
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'students.db')

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
''')

# Clear old records before inserting new records
cursor.execute("DELETE FROM students")

# Five sample student records
students = [
    ('2026-00230', 'IAN AUSTRIA', 'BSIT', 3, 'A'),
    ('2026-00188', 'JOHN MICLAEL', 'BSIT', 3, 'A'),
    ('2026-00125', 'RENIER CALAMBRO', 'BSIT', 3, 'A'),
    ('2026-00126', 'RAVEEN CELO', 'BSIT', 3, 'A'),
    ('2026-00127', 'Mark Lopez', 'BSIT', 3, 'B')
]

cursor.executemany('''
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
''', students)

conn.commit()
conn.close()

print("Database created successfully.")
