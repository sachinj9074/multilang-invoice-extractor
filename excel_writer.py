from datetime import date
from pathlib import Path

from openpyxl import Workbook, load_workbook

COLUMNS = [
    "Source Filename",
    "Date Processed",
    "Invoice Number",
    "Invoice Date",
    "Due Date",
    "PO Number",
    "Detected Language",
    "Currency",
    "Vendor Name",
    "Vendor Address",
    "Vendor Tax ID",
    "Vendor Contact",
    "Buyer Name",
    "Buyer Address",
    "Buyer Tax ID",
    "Subtotal",
    "Tax Amount",
    "Tax Type",
    "Discount",
    "Total Amount",
    "Payment Terms",
    "Confidence",
    "Flags",
]

FIELD_TO_COLUMN = {
    "invoice_number": "Invoice Number",
    "invoice_date": "Invoice Date",
    "due_date": "Due Date",
    "po_number": "PO Number",
    "detected_language": "Detected Language",
    "currency": "Currency",
    "vendor_name": "Vendor Name",
    "vendor_address": "Vendor Address",
    "vendor_tax_id": "Vendor Tax ID",
    "vendor_contact": "Vendor Contact",
    "buyer_name": "Buyer Name",
    "buyer_address": "Buyer Address",
    "buyer_tax_id": "Buyer Tax ID",
    "subtotal": "Subtotal",
    "tax_amount": "Tax Amount",
    "tax_type": "Tax Type",
    "discount": "Discount",
    "total_amount": "Total Amount",
    "payment_terms": "Payment Terms",
    "confidence": "Confidence",
}


def append_invoice_row(data, filename, excel_path="invoices.xlsx"):
    path = Path(excel_path)

    if path.exists():
        workbook = load_workbook(path)
        sheet = workbook.active
    else:
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(COLUMNS)

    row = {column: "" for column in COLUMNS}
    row["Source Filename"] = filename
    row["Date Processed"] = date.today().isoformat()

    if "error" in data:
        row["Flags"] = data["error"]
    else:
        for field, column in FIELD_TO_COLUMN.items():
            value = data.get(field)
            row[column] = value if value is not None else ""

        flags = data.get("flags") or []
        row["Flags"] = "; ".join(flags)

    sheet.append([row[column] for column in COLUMNS])
    workbook.save(path)
