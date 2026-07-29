import os
import customtkinter as ctk

from transaction_report import (
    generate_transaction_report
)

from income_expense_report import (
    generate_income_expense_report
)


def open_report_menu(app):

    report_window = ctk.CTkToplevel(app)

    report_window.title("Reports")

    report_window.geometry("500x300")

    title = ctk.CTkLabel(
        report_window,
        text="REPORTS",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    def business_report():

        file_path = (
            generate_transaction_report()
        )

        os.startfile(file_path)

    def income_expense_report():

        file_path = (
            generate_income_expense_report()
        )

        os.startfile(file_path)

    ctk.CTkButton(
        report_window,
        text="Business Report",
        width=300,
        height=50,
        command=business_report
    ).pack(pady=15)

    ctk.CTkButton(
        report_window,
        text="Income & Expenses Report",
        width=300,
        height=50,
        command=income_expense_report
    ).pack(pady=15)