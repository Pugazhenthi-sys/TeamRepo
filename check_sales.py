import sqlite3

conn = sqlite3.connect("billing_system.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    SELECT *
    FROM sales_register
    ORDER BY id DESC
    LIMIT 5
    """)

    rows = cursor.fetchall()

    print("ROWS FOUND:", len(rows))

    for row in rows:
        print(row)

except Exception as e:
    print("ERROR:", e)

conn.close()
