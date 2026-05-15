from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SHOW TABLES")

tables = cursor.fetchall()

print(tables)

conn.close()