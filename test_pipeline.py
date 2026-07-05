import sys
from pathlib import Path

from excel_writer import append_invoice_row
from extract import detect_media_type, extract_invoice_data
from validate import validate_invoice

sys.stdout.reconfigure(encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    filename = Path(image_path).name
    image_bytes = Path(image_path).read_bytes()
    media_type = detect_media_type(image_path)

    result = extract_invoice_data(image_bytes, media_type)
    result = validate_invoice(result)

    try:
        append_invoice_row(result, filename)
    except Exception as e:
        print(f"Failed to write row: {e}")
        sys.exit(1)

    if "error" in result:
        print(f"Row added, but extraction failed: {result['error']}")
    else:
        print("Row added successfully")


if __name__ == "__main__":
    main()
