import sqlite3

conn = sqlite3.connect("skillforge.db")

cursor = conn.cursor()

print("\n========== COURSES ==========")
cursor.execute("SELECT * FROM courses")
for row in cursor.fetchall():
    print(row)

print("\n========== MODULES ==========")
cursor.execute("SELECT * FROM modules")
for row in cursor.fetchall():
    print(row)

print("\n========== LESSONS ==========")
cursor.execute("SELECT * FROM lessons")
for row in cursor.fetchall():
    print(row)

conn.close()