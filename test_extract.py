import json
import sys
from pathlib import Path

from extract import detect_media_type, extract_invoice_data

sys.stdout.reconfigure(encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    image_bytes = Path(image_path).read_bytes()
    media_type = detect_media_type(image_path)

    result = extract_invoice_data(image_bytes, media_type)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
