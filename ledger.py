from database import conn, cursor
import customtkinter as ctk
from tkinter import messagebox


# ==========================================
# CREATE CUSTOMER
# ==========================================
def create_customer_if_not_exists(name):

    name = name.strip()

    cursor.execute("""
        SELECT id FROM customers WHERE name=?
    """, (name,))

    row = cursor.fetchone()

    if row:
        return row[0]

    cursor.execute("""
        INSERT INTO customers(name)
        VALUES(?)
    """, (name,))

    conn.commit()

    return cursor.lastrowid


# ==========================================
# ADD MONEY (CREDIT)
# ==========================================
def add_money(customer_id, amount, description, date):

    cursor.execute("""
        INSERT INTO transactions
        (customer_id, type, amount, description, date)
        VALUES (?, 'credit', ?, ?, ?)
    """, (customer_id, amount, description, date))

    conn.commit()


# ==========================================
# MINUS MONEY (DEBIT)
# ==========================================
def minus_money(customer_id, amount, description, date):

    cursor.execute("""
    INSERT INTO transactions
    (customer_id, type, amount, description, date)
    VALUES (?, 'debit', ?, ?, ?)
    """, (
        customer_id,
        amount,
        description,
        date
    ))

    cursor.execute("""
    SELECT name
    FROM customers
    WHERE id=?
    """, (customer_id,))

    customer_name = cursor.fetchone()[0]

    remaining = amount

    cursor.execute("""
    SELECT
        bill_no,
        bill_amount,
        paid_amount
    FROM bill_status
    WHERE customer_name=?
    AND status='Pending'
    ORDER BY bill_no ASC
    """, (customer_name,))

    bills = cursor.fetchall()

    for bill in bills:

        bill_no = bill[0]
        bill_amount = bill[1]
        paid_amount = bill[2]

        pending = bill_amount - paid_amount

        if remaining <= 0:
            break

        payment = min(
            remaining,
            pending
        )

        new_paid = paid_amount + payment

        remaining -= payment

        status = (
            "Completed"
            if new_paid >= bill_amount
            else "Pending"
        )

        cursor.execute("""
        UPDATE bill_status
        SET
            paid_amount=?,
            status=?
        WHERE bill_no=?
        """,
    (
        new_paid,
        status,
        bill_no
    ))

    conn.commit()


# ==========================================
# GET BALANCE
# ==========================================
def get_balance(customer_id):

    cursor.execute("""
        SELECT type, amount
        FROM transactions
        WHERE customer_id=?
    """, (customer_id,))

    rows = cursor.fetchall()

    balance = 0

    for ttype, amt in rows:

        if ttype == "credit":
            balance += amt
        else:
            balance -= amt

    return balance


# ==========================================
# GET HISTORY
# ==========================================
def get_history(customer_id):

    cursor.execute("""
        SELECT date, type, amount, description
        FROM transactions
        WHERE customer_id=?
        ORDER BY
        substr(date,7,4),   -- Year
        substr(date,4,2),   -- Month
        substr(date,1,2)    -- Day
        ASC
    """, (customer_id,))

    return cursor.fetchall()

# ==========================================
# GET CUSTOMERS
# ==========================================
def get_customers():

    cursor.execute("""
        SELECT id, name
        FROM customers
        ORDER BY name ASC
    """)

    return cursor.fetchall()


# ==========================================
# CUSTOMER MANAGEMENT UI
# ==========================================
def open_customer_management(parent):

    win = ctk.CTkToplevel(parent)
    win.title("Customer Management")
    win.geometry("1100x750")

    # LEFT PANEL (CUSTOMERS)
    left = ctk.CTkScrollableFrame(win, width=250)
    left.pack(side="left", fill="y", padx=10, pady=10)

    # RIGHT PANEL
    right = ctk.CTkFrame(win)
    right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    title = ctk.CTkLabel(right, text="Select Customer", font=("Arial", 20, "bold"))
    title.pack(pady=10)

    # ==========================================
    # BALANCE + BUTTONS ROW
    # ==========================================

    top_frame = ctk.CTkFrame(
        right,
        fg_color="#1f1f1f"
    )

    top_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    balance_title = ctk.CTkLabel(
        top_frame,
        text="CURRENT BALANCE :",
        font=("Arial", 16, "bold")
    )

    balance_title.pack(
        side="left",
        padx=(20, 5),
        pady=10
    )

    balance_label = ctk.CTkLabel(
        top_frame,
        text="₹0.00",
        font=("Arial", 20, "bold")
    )

    balance_label.pack(
        side="left",
        padx=(0, 30)
    )

    
    # TRANSACTION HISTORY TITLE

    ctk.CTkLabel(
        right,
        text="TRANSACTION HISTORY",
        font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))

    history_box = ctk.CTkScrollableFrame(
        right,
        height=250
    )

    history_box.pack(
        fill="x",
        padx=10,
        pady=5
    )

    
    # ==========================================
    # BILL STATUS AREA
    # ==========================================

    bill_status_title = ctk.CTkLabel(
        right,
        text="BILLS COMPLETION STATUS",
        font=("Arial", 18, "bold")
    )

    bill_status_title.pack(pady=(10, 5))

    bill_status_box = ctk.CTkScrollableFrame(
        right,
        height=220
    )

    bill_status_box.pack(
        fill="x",
        padx=10,
        pady=5
    )
    

    selected = {"id": None}

    # ==========================================
    # LOAD DATA (BALANCE + HISTORY)
    # ==========================================
    def load_data(cid):

        bal = get_balance(cid)

        balance_label.configure(text=f"₹{bal:.2f}")

        if bal > 0:
            balance_label.configure(text_color="green")
        elif bal < 0:
            balance_label.configure(text_color="red")
        else:
            balance_label.configure(text_color="white")

        for w in history_box.winfo_children():
            w.destroy()

        rows = get_history(cid)

        if not rows:
            ctk.CTkLabel(history_box, text="No Transactions Found").pack()
            return

        for date, ttype, amt, desc in rows:

            sign = "+" if ttype == "credit" else "-"

            text = f"{date} | {sign}₹{amt:.2f} | {desc}"

            ctk.CTkLabel(history_box, text=text, anchor="w").pack(fill="x", pady=2)
    def load_bill_status(customer_name):

        for w in bill_status_box.winfo_children():
            w.destroy()

        cursor.execute("""
        SELECT
            bs.bill_no,
            sr.particular,
            bs.bill_amount,
            bs.paid_amount,
            bs.status
        FROM bill_status bs
        LEFT JOIN sales_register sr
        ON bs.bill_no = sr.bill_no
        WHERE bs.customer_name=?
        ORDER BY bs.bill_no
        """, (customer_name,))

        rows = cursor.fetchall()

        if not rows:

            ctk.CTkLabel(
                bill_status_box,
                text="No Bills Found"
            ).pack(pady=10)

            return

        for row in rows:

            bill_no = row[0]
            particular = row[1]
            bill_amount = row[2]
            paid_amount = row[3]
            status = row[4]

            balance = bill_amount - paid_amount

            status_text = (
                "✅ COMPLETED"
                if status == "Completed"
                else "🔴 PENDING"
            )

            text = (
                f"Bill No : {bill_no}\n"
                f"Particular : {particular}\n"
                f"Status : {status_text}\n"
                f"Balance : ₹{balance:,.2f}"
            )
            card = ctk.CTkFrame(
                bill_status_box
            )

            card.pack(
                fill="x",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=text,
                justify="left",
                anchor="w",
                font=("Arial", 14)
            ).pack(
                anchor="w",
                padx=10,
                pady=10
            )
    # ==========================================
    # SELECT CUSTOMER
    # ==========================================
    def select_customer(cid, name):

        selected["id"] = cid

        title.configure(
            text=name.upper()
        )

        load_data(cid)

        load_bill_status(name)

    # ==========================================
    # LOAD CUSTOMER LIST
    # ==========================================
    def load_customers():

        for w in left.winfo_children():
            w.destroy()

        for cid, name in get_customers():

            ctk.CTkButton(
                left,
                text=name,
                command=lambda i=cid, n=name: select_customer(i, n)
            ).pack(fill="x", pady=2)

    # ==========================================
    # ADD MONEY WINDOW
    # ==========================================
    def open_add():

        if not selected["id"]:
            messagebox.showerror("Error", "Select customer first")
            return

        pop = ctk.CTkToplevel(win)
        pop.title("Add Money")
        pop.geometry("300x250")

        date = ctk.CTkEntry(pop, placeholder_text="Date (DD-MM-YYYY)")
        date.pack(pady=5)

        amount = ctk.CTkEntry(pop, placeholder_text="Amount")
        amount.pack(pady=5)

        desc = ctk.CTkEntry(pop, placeholder_text="Description")
        desc.pack(pady=5)

        def save():

            add_money(
                selected["id"],
                float(amount.get()),
                desc.get(),
                date.get()
            )

            pop.destroy()
            load_data(selected["id"])

            cursor.execute("""
            SELECT name
            FROM customers
            WHERE id=?
            """, (selected["id"],))

            customer_name = cursor.fetchone()[0]

            load_bill_status(customer_name)

        ctk.CTkButton(pop, text="Add Money", command=save).pack(pady=10)

    # ==========================================
    # MINUS MONEY WINDOW
    # ==========================================
    def open_minus():

        if not selected["id"]:
            messagebox.showerror("Error", "Select customer first")
            return

        pop = ctk.CTkToplevel(win)
        pop.title("Minus Money")
        pop.geometry("300x250")

        date = ctk.CTkEntry(pop, placeholder_text="Date (DD-MM-YYYY)")
        date.pack(pady=5)

        amount = ctk.CTkEntry(pop, placeholder_text="Paid Amount")
        amount.pack(pady=5)

        desc = ctk.CTkEntry(pop, placeholder_text="Description")
        desc.pack(pady=5)

        def save():

            minus_money(
                selected["id"],
                float(amount.get()),
                desc.get(),
                date.get()
            )

            pop.destroy()

            load_data(selected["id"])

            cursor.execute("""
            SELECT name
            FROM customers
            WHERE id=?
            """, (selected["id"],))

            customer_name = cursor.fetchone()[0]

            load_bill_status(customer_name)
        ctk.CTkButton(
            pop,
            text="Minus Money",
            command=save
        ).pack(pady=10)
            


    btn_frame = ctk.CTkFrame(top_frame)
    btn_frame.pack(side="right", padx=10)

    ctk.CTkButton(
        btn_frame,
        text="➕ Add Money",
        width=120,
        command=open_add
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="➖ Minus Money",
        width=120,
        command=open_minus
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="Close",
        width=100,
        fg_color="red",
        command=win.destroy
    ).pack(side="left", padx=5)
    # INIT LOAD
    load_customers()