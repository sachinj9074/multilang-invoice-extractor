import base64
import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MASTER_PROMPT = """You are an invoice data extraction assistant. You will be shown an image of an
invoice, in any language and any layout. Extract the following fields exactly
as specified and return ONLY a valid JSON object — no markdown code fences, no
explanation before or after, nothing except the JSON.

Fields:
- invoice_number (string or null)
- invoice_date (string, format YYYY-MM-DD, or null if not present/ambiguous)
- due_date (string, format YYYY-MM-DD, or null)
- po_number (string or null)
- detected_language (string, e.g. "Spanish")
- currency (string, ISO 4217 code e.g. "INR", "USD", "EUR", or null)
- vendor_name (string or null)
- vendor_address (string or null)
- vendor_tax_id (string or null)
- vendor_contact (string or null)
- buyer_name (string or null)
- buyer_address (string or null)
- buyer_tax_id (string or null)
- subtotal (number or null, no currency symbols or thousands separators)
- tax_amount (number or null, same formatting)
- tax_type (string or null, e.g. "GST 18%")
- discount (number or null, same formatting)
- total_amount (number or null, same formatting)
- payment_terms (string or null)
- confidence ("high", "medium", or "low")
- flags (array of strings noting any issues, e.g. "handwritten total"; [] if none)

Rules:
- If a field is not present or cannot be read confidently, use null. Never guess.
- Assume exactly one invoice per image.
- Output must be valid JSON and nothing else."""

MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}


def detect_media_type(filename):
    media_type = MEDIA_TYPES.get(Path(filename).suffix.lower())
    if media_type is None:
        raise ValueError(f"Unsupported image extension: {Path(filename).suffix}")
    return media_type


def extract_invoice_data(image_bytes, media_type):
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Set it in a local .env file, "
            "or as an environment variable / secret in the deployment environment."
        )

    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": MASTER_PROMPT,
                    },
                ],
            }
        ],
    )

    raw_text = next(
        block.text for block in response.content if block.type == "text"
    )

    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.strip("`")
        if cleaned_text.startswith("json"):
            cleaned_text = cleaned_text[len("json"):]
        cleaned_text = cleaned_text.strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON: {e}", "raw_response": raw_text}
