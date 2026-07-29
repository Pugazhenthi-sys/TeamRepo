# ==========================================
# app.py
# COMPLETE FINAL APP
# ==========================================

import os
import shutil

import customtkinter as ctk

from tkinter import (
    messagebox,
    filedialog,
    ttk
)

from billing import (
    generate_bill_gui
)

from ledger import (
    open_customer_management
)

from dashboard import (
    open_dashboard
)
from expenses import (
    open_expense_calculator
)
from report_menu import (
    open_report_menu
)


# ==========================================
# APP SETTINGS
# ==========================================

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")

# ==========================================
# MAIN APP
# ==========================================

app = ctk.CTk()

app.title(
    "SSS Software"
)

app.geometry("1000x800")

# ==========================================
# TITLE
# ==========================================

title = ctk.CTkLabel(
    app,
    text="AGILE PROJECT",
    font=("Arial", 32, "bold")
)

title.pack(pady=20)


# ==========================================
# MAIN FRAME
# ==========================================

main_frame = ctk.CTkFrame(app)

main_frame.pack(
    pady=30,
    padx=30,
    fill="both",
    expand=True
)

# ==========================================
# GENERATE BILL WINDOW
# ==========================================

def open_generate_bill():

    bill_window = ctk.CTkToplevel(app)

    bill_window.title("Generate Bill")

    bill_window.geometry("550x900")

    # ======================================
    # TITLE
    # ======================================

    heading = ctk.CTkLabel(
        bill_window,
        text="GENERATE BILL",
        font=("Arial", 28, "bold")
    )

    heading.pack(pady=20)

    # ======================================
    # CUSTOMER NAME
    # ======================================

    vendor_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Customer Name",
        width=400,
        height=45
    )

    vendor_entry.pack(pady=10)

    # ======================================
    # DATE
    # ======================================

    date_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Date (DD-MM-YYYY)",
        width=400,
        height=45
    )

    date_entry.pack(pady=10)

    # ======================================
    # BAGS
    # ======================================

    bags_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Number of Bags",
        width=400,
        height=45
    )

    bags_entry.pack(pady=10)

    # ======================================
    # BAG SIZE
    # ======================================

    bag_size_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Bag Size (kg)",
        width=400,
        height=45
    )

    bag_size_entry.pack(pady=10)

    # ======================================
    # PARTICULAR
    # ======================================

    particular_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Rice Brand / Particular",
        width=400,
        height=45
    )

    particular_entry.pack(pady=10)

    # ======================================
    # SELLING RATE
    # ======================================

    rate_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Selling Rate Per Kg",
        width=400,
        height=45
    )

    rate_entry.pack(pady=10)

    # ======================================
    # PURCHASE RATE
    # ======================================

    purchase_rate_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Purchase Rate Per Kg",
        width=400,
        height=45
    )

    purchase_rate_entry.pack(pady=10)

    # ======================================
    # DUTY PER KG
    # ======================================

    duty_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Duty Per Kg",
        width=400,
        height=45
    )

    duty_entry.pack(pady=10)

    # ======================================
    # VEHICLE NUMBER
    # ======================================

    vehicle_entry = ctk.CTkEntry(
        bill_window,
        placeholder_text="Vehicle Number",
        width=400,
        height=45
    )

    vehicle_entry.pack(pady=10)

    # ======================================
    # GENERATE BILL FUNCTION
    # ======================================

    def generate_bill_action():

        try:

            vendor_name = (
                vendor_entry.get()
            )

            date = (
                date_entry.get()
            )

            bags = int(
                bags_entry.get()
            )

            bag_size = float(
                bag_size_entry.get()
            )

            particular = (
                particular_entry.get()
            )

            rate = float(
                rate_entry.get()
            )

            purchase_rate = float(
                purchase_rate_entry.get()
            )

            duty_per_kg = float(
                duty_entry.get()
            )

            vehicle_no = (
                vehicle_entry.get()
            )

            result = generate_bill_gui(
                vendor_name,
                date,
                bags,
                bag_size,
                particular,
                rate,
                purchase_rate,
                duty_per_kg,
                vehicle_no
            )

            (
                excel_file,
                pdf_file,
                balance,
                profit
            ) = result

            messagebox.showinfo(
                "Success",
                f"Bill Generated Successfully\n\n"
                f"Balance : ₹{balance:.2f}\n"
                f"Profit : ₹{profit:.2f}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ======================================
    # GENERATE BUTTON
    # ======================================

    generate_btn = ctk.CTkButton(
        bill_window,
        text="Generate Bill",
        width=400,
        height=55,
        font=("Arial", 22, "bold"),
        command=generate_bill_action
    )

    generate_btn.pack(pady=30)

# ==========================================
# VIEW BILLS
# ==========================================

def open_view_bills():

    bills_window = ctk.CTkToplevel(app)

    bills_window.title("View Bills")

    bills_window.geometry("1000x750")

    title = ctk.CTkLabel(
        bills_window,
        text="ALL BILLS",
        font=("Arial", 30, "bold")
    )

    title.pack(pady=20)

    # ======================================
    # SEARCH
    # ======================================

    search_entry = ctk.CTkEntry(
        bills_window,
        placeholder_text="Search Customer",
        width=400,
        height=40
    )

    search_entry.pack(pady=10)

    # ======================================
    # SCROLL FRAME
    # ======================================

    bills_frame = ctk.CTkScrollableFrame(
        bills_window,
        width=900,
        height=550
    )

    bills_frame.pack(
        pady=20,
        padx=20,
        fill="both",
        expand=True
    )

    # ======================================
    # OPEN FILE
    # ======================================

    def open_file(path):

        try:

            os.startfile(path)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ======================================
    # LOAD BILLS
    # ======================================

    def load_bills(search_text=""):

        for widget in bills_frame.winfo_children():

            widget.destroy()

        base_path = "data/vendors"

        if not os.path.exists(base_path):

            return

        for vendor_folder in os.listdir(base_path):

            vendor_name = vendor_folder.replace(
                "vendor_",
                ""
            )

            if (
                search_text.lower()
                not in vendor_name.lower()
            ):
                continue

            excel_folder = os.path.join(
                base_path,
                vendor_folder,
                "invoices",
                "generated"
            )

            pdf_folder = os.path.join(
                base_path,
                vendor_folder,
                "pdf_bills"
            )

            if not os.path.exists(excel_folder):

                continue

            excel_files = sorted(
                os.listdir(excel_folder),
                reverse=True
            )

            # ==============================
            # CUSTOMER TITLE
            # ==============================

            customer_label = ctk.CTkLabel(
                bills_frame,
                text=vendor_name.upper(),
                font=("Arial", 24, "bold")
            )

            customer_label.pack(
                pady=10
            )

            # ==============================
            # FILES
            # ==============================

            for excel_file in excel_files:

                bill_frame = ctk.CTkFrame(
                    bills_frame
                )

                bill_frame.pack(
                    fill="x",
                    pady=5,
                    padx=10
                )

                bill_label = ctk.CTkLabel(
                    bill_frame,
                    text=excel_file,
                    font=("Arial", 16)
                )

                bill_label.pack(
                    side="left",
                    padx=10,
                    pady=10
                )

                excel_path = os.path.join(
                    excel_folder,
                    excel_file
                )

                pdf_name = (
                    excel_file
                    .replace(".xlsx", ".pdf")
                    .replace(
                        vendor_name.lower(),
                        "bill"
                    )
                )

                pdf_path = os.path.join(
                    pdf_folder,
                    pdf_name
                )

                # ==========================
                # OPEN EXCEL BUTTON
                # ==========================

                excel_btn = ctk.CTkButton(
                    bill_frame,
                    text="Open Excel",
                    width=120,
                    command=lambda
                    p=excel_path:
                    open_file(p)
                )

                excel_btn.pack(
                    side="right",
                    padx=5
                )

                # ==========================
                # OPEN PDF BUTTON
                # ==========================

                pdf_btn = ctk.CTkButton(
                    bill_frame,
                    text="Open PDF",
                    width=120,
                    fg_color="green",
                    command=lambda
                    p=pdf_path:
                    open_file(p)
                )

                pdf_btn.pack(
                    side="right",
                    padx=5
                )

    # ======================================
    # SEARCH FUNCTION
    # ======================================

    def search_bill(event):

        load_bills(
            search_entry.get()
        )

    search_entry.bind(
        "<KeyRelease>",
        search_bill
    )

    # ======================================
    # INITIAL LOAD
    # ======================================

    load_bills()

# ==========================================
# BACKUP FUNCTION
# ==========================================

def create_backup():

    try:

        backup_folder = filedialog.askdirectory()

        if not backup_folder:

            return

        source = "data"

        destination = os.path.join(
            backup_folder,
            "RiceMillBackup"
        )

        if os.path.exists(destination):

            shutil.rmtree(destination)

        shutil.copytree(
            source,
            destination
        )

        messagebox.showinfo(
            "Success",
            "Backup Created Successfully"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

# ==========================================
# BUTTONS
# ==========================================

generate_bill_btn = ctk.CTkButton(
    main_frame,
    text="Generate Bill",
    width=350,
    height=60,
    font=("Arial", 22),
    command=open_generate_bill
)

generate_bill_btn.pack(pady=15)

view_bills_btn = ctk.CTkButton(
    main_frame,
    text="View Bills",
    width=350,
    height=60,
    font=("Arial", 22),
    command=open_view_bills
)

view_bills_btn.pack(pady=15)

customer_btn = ctk.CTkButton(
    main_frame,
    text="Customer Management",
    width=350,
    height=60,
    font=("Arial", 22),
    command=lambda:
    open_customer_management(app)
)


customer_btn.pack(pady=15)

dashboard_btn = ctk.CTkButton(
    main_frame,
    text="Dashboard",
    width=350,
    height=60,
    font=("Arial", 22),
    command=lambda:
    open_dashboard(app)
)

dashboard_btn.pack(pady=15)
expense_btn = ctk.CTkButton(
    main_frame,
    text="Expense Calculator",
    width=350,
    height=60,
    font=("Arial", 22),
    command=lambda:
    open_expense_calculator(app)
)

expense_btn.pack(pady=15)
report_btn = ctk.CTkButton(
    main_frame,
    text="Transaction Report",
    width=350,
    height=60,
    font=("Arial", 22),
    fg_color="orange",
    command=lambda:
    open_report_menu(app)
)

report_btn.pack(pady=15)

backup_btn = ctk.CTkButton(
    main_frame,
    text="Create Backup",
    width=350,
    height=60,
    font=("Arial", 22),
    fg_color="green",
    command=create_backup
)

backup_btn.pack(pady=15)

# ==========================================
# RUN APP
# ==========================================

app.mainloop()
