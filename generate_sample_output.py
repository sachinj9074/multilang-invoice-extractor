from pathlib import Path

from excel_writer import append_invoice_row

OUTPUT_PATH = "sample_output.xlsx"

ROWS = [
    (
        "sample_invoice_001.jpg",
        {
            "invoice_number": "INV-2026-0142",
            "invoice_date": "2026-05-12",
            "due_date": "2026-06-11",
            "po_number": "PO-88213",
            "detected_language": "English",
            "currency": "USD",
            "vendor_name": "Brightfield Office Supplies LLC",
            "vendor_address": "48 Maple Ridge Drive, Suite 200, Springfield, IL 62704",
            "vendor_tax_id": "37-4419021",
            "vendor_contact": "billing@brightfieldsupplies.example",
            "buyer_name": "Harlow & Reed Consulting",
            "buyer_address": "1290 Cedar Grove Ave, Springfield, IL 62701",
            "buyer_tax_id": "45-1183302",
            "subtotal": 2400.00,
            "tax_amount": 192.00,
            "tax_type": "Sales Tax 8%",
            "discount": None,
            "total_amount": 2592.00,
            "payment_terms": "Net 30",
            "confidence": "high",
            "flags": [],
        },
    ),
    (
        "sample_invoice_002.jpg",
        {
            "invoice_number": "7",
            "invoice_date": "2026-02-03",
            "due_date": None,
            "po_number": None,
            "detected_language": "Hindi",
            "currency": "INR",
            "vendor_name": "सूर्या ट्रेडर्स",
            "vendor_address": "दुकान नं. 12, सदर बाज़ार, जयपुर, राजस्थान 302003",
            "vendor_tax_id": "08BZTPS4521Q1ZK",
            "vendor_contact": None,
            "buyer_name": "अनिल शर्मा",
            "buyer_address": "मकान नं. 45, गांधी नगर, जयपुर, राजस्थान",
            "buyer_tax_id": None,
            "subtotal": 8600.00,
            "tax_amount": 430.00,
            "tax_type": "GST 5%",
            "discount": None,
            "total_amount": 9030.00,
            "payment_terms": None,
            "confidence": "medium",
            "flags": ["buyer tax ID missing"],
        },
    ),
    (
        "sample_invoice_003.jpg",
        {
            "invoice_number": "INV-55031",
            "invoice_date": "2026-01-20",
            "due_date": "2026-02-19",
            "po_number": "PO-4471",
            "detected_language": "English",
            "currency": "USD",
            "vendor_name": "Coastal Print & Signage Co.",
            "vendor_address": "220 Harbor View Road, Newport, OR 97365",
            "vendor_tax_id": "91-2287744",
            "vendor_contact": "accounts@coastalprintco.example",
            "buyer_name": "Driftwood Realty Group",
            "buyer_address": "76 Lighthouse Lane, Newport, OR 97365",
            "buyer_tax_id": "82-6650912",
            "subtotal": 1150.00,
            "tax_amount": 92.00,
            "tax_type": "Sales Tax 8%",
            "discount": None,
            "total_amount": 1300.00,
            "payment_terms": "Net 15",
            "confidence": "low",
            "flags": ["total does not match subtotal + tax"],
        },
    ),
]


def main():
    output_path = Path(OUTPUT_PATH)
    if output_path.exists():
        output_path.unlink()

    for filename, data in ROWS:
        append_invoice_row(data, filename, excel_path=OUTPUT_PATH)

    print("Sample file created")


if __name__ == "__main__":
    main()
