import sqlite3
conn = sqlite3.connect('database.db')
result = conn.execute('SELECT DISTINCT difficulty FROM questions').fetchall()
print("In database:", result)