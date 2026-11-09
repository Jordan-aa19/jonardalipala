
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'students.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

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

cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")

students = [
    ('2026-00123', 'Juan Dela Cruz', 'BSIT', 1, 'A'),
    ('2026-00124', 'Maria Santos', 'BSIT', 1, 'A'),
    ('2026-00125', 'Pedro Reyes', 'BSIT', 2, 'B'),
    ('2026-00126', 'Ana Garcia', 'BSCS', 2, 'B'),
    ('2026-00127', 'Mark Lopez', 'BSIT', 3, 'C')
]

cursor.executemany('''
INSERT INTO students
(student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
''', students)

conn.commit()
conn.close()

print("Database created successfully.")
