import customtkinter as ctk

from tkinter import messagebox

from database import conn, cursor


def open_expense_calculator(app):

    expense_window = ctk.CTkToplevel(app)

    expense_window.title("Expense Calculator")

    expense_window.geometry("500x450")

    # =====================================
    # TITLE
    # =====================================

    title = ctk.CTkLabel(
        expense_window,
        text="EXPENSE CALCULATOR",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    # =====================================
    # DATE
    # =====================================

    date_entry = ctk.CTkEntry(
        expense_window,
        placeholder_text="Date (DD-MM-YYYY)",
        width=350,
        height=45
    )

    date_entry.pack(pady=10)

    # =====================================
    # DESCRIPTION
    # =====================================

    description_entry = ctk.CTkEntry(
        expense_window,
        placeholder_text="Description",
        width=350,
        height=45
    )

    description_entry.pack(pady=10)

    # =====================================
    # AMOUNT
    # =====================================

    amount_entry = ctk.CTkEntry(
        expense_window,
        placeholder_text="Amount",
        width=350,
        height=45
    )

    amount_entry.pack(pady=10)

    # =====================================
    # SAVE EXPENSE
    # =====================================

    def save_expense():

        try:

            date = date_entry.get().strip()

            description = (
                description_entry
                .get()
                .strip()
            )

            amount = float(
                amount_entry.get()
            )

            if not date:

                raise Exception(
                    "Enter Date"
                )

            if not description:

                raise Exception(
                    "Enter Description"
                )

            cursor.execute("""
            INSERT INTO expenses
            (
                date,
                description,
                amount
            )
            VALUES (?, ?, ?)
            """, (
                date,
                description,
                amount
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Expense Saved Successfully"
            )

            date_entry.delete(0, "end")
            description_entry.delete(0, "end")
            amount_entry.delete(0, "end")

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================
    # SAVE BUTTON
    # =====================================

    save_btn = ctk.CTkButton(
        expense_window,
        text="Save Expense",
        width=350,
        height=50,
        font=("Arial", 20, "bold"),
        command=save_expense
    )

    save_btn.pack(pady=30)
