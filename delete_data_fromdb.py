from database import conn, cursor

bill_no = 23

cursor.execute(
    "DELETE FROM sales_register WHERE bill_no=?",
    (bill_no,)
)

cursor.execute(
    "DELETE FROM income WHERE bill_no=?",
    (bill_no,)
)

cursor.execute(
    "DELETE FROM bill_status WHERE bill_no=?",
    (bill_no,)
)

cursor.execute(
    "DELETE FROM transactions WHERE description=?",
    (f"Bill No {bill_no}",)
)

conn.commit()

print("Bill deleted successfully")
