import json
import sys

from extract import extract_invoice_data

sys.stdout.reconfigure(encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    result = extract_invoice_data(image_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
