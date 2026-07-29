import customtkinter as ctk

from tkinter import ttk

from database import cursor

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

from matplotlib.figure import Figure

# ==========================================
# DASHBOARD WINDOW
# ==========================================

def open_dashboard(app):

    dashboard = ctk.CTkToplevel(app)

    dashboard.title("Analytics Dashboard")

    dashboard.geometry("1400x850")
  
    # ======================================
    # TITLE
    # ======================================

    title = ctk.CTkLabel(
        dashboard,
        text="BUSINESS ANALYTICS",
        font=("Arial", 34, "bold")
    )

    title.pack(pady=20)

    # ======================================
    # TOP STATS FRAME
    # ======================================

    stats_frame = ctk.CTkFrame(
        dashboard
    )

    stats_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    # ======================================
    # TOTAL CUSTOMERS
    # ======================================

    cursor.execute("""
    SELECT COUNT(*)
    FROM customers
    """)

    total_customers = cursor.fetchone()[0]

    # ======================================
    # TOTAL BALANCE
    # ======================================

    cursor.execute("""
    SELECT type, amount
    FROM transactions
    """)

    transactions = cursor.fetchall()

    total_balance = 0

    for t in transactions:

        if t[0] == "credit":

            total_balance += t[1]

        else:

            total_balance -= t[1]

    
    # ======================================
    # TOTAL BILLS
    # ======================================

    cursor.execute("""
    SELECT COUNT(*)
    FROM income
    """)

    total_bills = cursor.fetchone()[0]
    # ======================================
    # TOTAL PENDING BALANCE
    # ======================================

    cursor.execute("""
    SELECT id
    FROM customers
    """)

    customer_ids = cursor.fetchall()

    total_pending = 0

    for customer in customer_ids:

        customer_id = customer[0]

        cursor.execute("""
        SELECT type, amount
        FROM transactions
        WHERE customer_id=?
        """, (customer_id,))

        transactions = cursor.fetchall()

        balance = 0

        for t in transactions:

            if t[0] == "credit":
                balance += t[1]
            else:
                balance -= t[1]

        if balance > 0:
            total_pending += balance

    # ======================================
    # PENDING PROFIT
    # ======================================

    cursor.execute("""
    SELECT SUM(profit)
    FROM bill_status
    WHERE status='Pending'
    """)

    result = cursor.fetchone()[0]

    pending_profit = (
        result if result else 0
    )
    # ======================================
    # REALIZED PROFIT
    # ======================================

    cursor.execute("""
    SELECT SUM(profit)
    FROM bill_status
    WHERE status='Completed'
    """)

    result = cursor.fetchone()[0]

    realized_profit = (
        result if result else 0
    )

    # ======================================
    # CARD FUNCTION
    # ======================================

    def create_card(
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            width=220,
            height=120
        )

        card.pack(
            side="left",
            padx=15,
            pady=15
        )

        card.pack_propagate(False)

        label1 = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 20, "bold")
        )

        label1.pack(pady=10)

        label2 = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 26)
        )

        label2.pack(pady=5)

    # ======================================
    # CARDS
    # ======================================

    create_card(
        stats_frame,
        "Customers",
        str(total_customers)
    )

    create_card(
        stats_frame,
        "Outstandings",
        f"₹{total_balance:.2f}"
    )
    

    create_card(
        stats_frame,
        "Pending Profit",
        f"₹{pending_profit:.2f}"
    )


    create_card(
        stats_frame,
        "Bills",
        str(total_bills)
    )

    create_card(
        stats_frame,
        "Realized Profit",
        f"₹{realized_profit:.2f}"
    )

    # ======================================
    # GRAPH FRAME
    # ======================================

    graph_frame = ctk.CTkFrame(
        dashboard
    )

    graph_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ======================================
    # MONTHLY PROFIT GRAPH
    # ======================================

    cursor.execute("""
    SELECT
        substr(date,4,7),
        SUM(profit)
    FROM income
    GROUP BY substr(date,4,7)
    """)

    data = cursor.fetchall()

    months = []
    profits = []

    for row in data:

        months.append(row[0])

        profits.append(row[1])

    fig = Figure(
        figsize=(6, 4),
        dpi=100
    )

    ax = fig.add_subplot(111)

    ax.plot(
        months,
        profits,
        marker='o'
    )

    ax.set_title(
        "Monthly Profit"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Profit"
    )

    canvas = FigureCanvasTkAgg(
        fig,
        master=graph_frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        side="left",
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ======================================
    # TOP BUYERS
    # ======================================

    cursor.execute("""
    SELECT
        customer_name,
        SUM(profit)
    FROM income
    GROUP BY customer_name
    ORDER BY SUM(profit) DESC
    LIMIT 5
    """)

    buyers = cursor.fetchall()

    buyer_frame = ctk.CTkScrollableFrame(
    graph_frame,
    width=350,
    height=700
)

    buyer_frame.pack(
        side="right",
        fill="y",
        padx=20,
        pady=20
    )
    title = ctk.CTkLabel(
        buyer_frame,
        text="TOP BUYERS",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=20)

    for buyer in buyers:

        label = ctk.CTkLabel(
            buyer_frame,
            text=
            f"{buyer[0]} : ₹{buyer[1]:.2f}",
            font=("Arial", 18)
        )

        label.pack(
            pady=10
        )

    # ======================================
    # PENDING CUSTOMERS
    # ======================================

    pending_title = ctk.CTkLabel(
        buyer_frame,
        text="PENDING CUSTOMERS",
        font=("Arial", 24, "bold")
    )

    pending_title.pack(pady=20)

    cursor.execute("""
    SELECT id, name
    FROM customers
    """)

    customers = cursor.fetchall()

    for customer in customers:

        customer_id = customer[0]

        customer_name = customer[1]

        cursor.execute("""
        SELECT type, amount
        FROM transactions
        WHERE customer_id=?
        """, (customer_id,))

        transactions = cursor.fetchall()

        balance = 0

        for t in transactions:

            if t[0] == "credit":

                balance += t[1]

            else:

                balance -= t[1]

        if balance > 0:

            label = ctk.CTkLabel(
                buyer_frame,
                text=
                f"{customer_name} : ₹{balance:.2f}",
                font=("Arial", 16)
            )

            label.pack(pady=5)
