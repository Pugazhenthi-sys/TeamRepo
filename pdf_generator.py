import os

from fpdf import FPDF

# ==========================================
# CREATE PDF BILL
# ==========================================

def generate_pdf_bill(
    vendor_name,
    bill_no,
    date,
    bags,
    bag_size,
    particular,
    weight,
    rate,
    amount,
    lorry_rent,
    final_bill,
    total_balance,
    vehicle_no
):

    # ======================================
    # PDF FOLDER
    # ======================================

    pdf_folder = os.path.join(
        "data/vendors",
        f"vendor_{vendor_name}",
        "pdf_bills"
    )

    os.makedirs(
        pdf_folder,
        exist_ok=True
    )

    # ======================================
    # PDF FILE NAME
    # ======================================

    pdf_file = os.path.join(
        pdf_folder,
        f"bill_{str(bill_no).zfill(3)}.pdf"
    )

    # ======================================
    # CREATE PDF
    # ======================================

    pdf = FPDF()

    pdf.add_page()

    # ======================================
    # TITLE
    # ======================================

    pdf.set_font(
        "Arial",
        "B",
        18
    )

    pdf.cell(
        200,
        10,
        "SHREE SAI SARAVANABHAVA TRADERS",
        ln=True,
        align="C"
    )

    pdf.set_font(
        "Arial",
        "",
        12
    )

    pdf.cell(
        200,
        8,
        "Rice Merchants",
        ln=True,
        align="C"
    )

    pdf.cell(
        200,
        8,
        "GSTIN: 33BFIPM8973G1Z1",
        ln=True,
        align="C"
    )

    pdf.cell(
        200,
        8,
        "Phone: 7904434418",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # ======================================
    # BILL DETAILS
    # ======================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        100,
        10,
        f"Bill No : {bill_no}"
    )

    pdf.cell(
        100,
        10,
        f"Date : {date}",
        ln=True
    )

    pdf.cell(
        100,
        10,
        f"Customer : {vendor_name}",
        ln=True
    )

    pdf.ln(5)

    # ======================================
    # TABLE HEADER
    # ======================================

    pdf.set_font(
        "Arial",
        "B",
        11
    )

    pdf.cell(
        35,
        10,
        "Bags",
        border=1
    )

    pdf.cell(
        50,
        10,
        "Particular",
        border=1
    )

    pdf.cell(
        35,
        10,
        "Qty",
        border=1
    )

    pdf.cell(
        30,
        10,
        "Rate",
        border=1
    )

    pdf.cell(
        40,
        10,
        "Amount",
        border=1,
        ln=True
    )

    # ======================================
    # TABLE DATA
    # ======================================

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.cell(
        35,
        10,
        f"{bags} ({bag_size}kg)",
        border=1
    )

    pdf.cell(
        50,
        10,
        particular,
        border=1
    )

    pdf.cell(
        35,
        10,
        str(weight),
        border=1
    )

    pdf.cell(
        30,
        10,
        str(rate),
        border=1
    )

    pdf.cell(
        40,
        10,
        f"Rs{amount:.2f}",
        border=1,
        ln=True
    )

    pdf.ln(10)

    # ======================================
    # BILL SUMMARY
    # ======================================

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        80,
        10,
        f"Lorry Rent : Rs{lorry_rent:.2f}",
        ln=True
    )

    pdf.cell(
        80,
        10,
        f"Final Bill : Rs{final_bill:.2f}",
        ln=True
    )

    pdf.cell(
        80,
        10,
        f"Total Balance : Rs{total_balance:.2f}",
        ln=True
    )

    pdf.ln(10)

    # ======================================
    # VEHICLE NUMBER
    # ======================================

    pdf.cell(
        80,
        10,
        f"Vehicle No : {vehicle_no}",
        ln=True
    )

    pdf.ln(20)
    # ======================================
    # SIGNATURE IMAGE
    # ======================================

    signature_path = r"D:\SOFTWARE M\signature.PNG"

    if os.path.exists(signature_path):
        pdf.image(
            signature_path,
            x=150,          # Adjust if needed
            y=pdf.get_y(),
            w=40            # Adjust size if needed
        )

    pdf.ln(15)

    pdf.cell(
        150,
        10,
        ""
    )

    pdf.cell(
        40,
        10,
        "Authorized Signature"
    )

    pdf.ln(10)

    pdf.cell(
        150,
        10,
        ""
    )


    # ======================================
    # SAVE PDF
    # ======================================

    pdf.output(pdf_file)

    return pdf_file