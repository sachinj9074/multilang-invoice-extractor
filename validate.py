def validate_invoice(data):
    if "error" in data:
        data["arithmetic_check"] = "not_verifiable"
        data["needs_review"] = "Y"
        return data

    subtotal = data.get("subtotal")
    tax_amount = data.get("tax_amount")
    total_amount = data.get("total_amount")

    if subtotal is not None and tax_amount is not None and total_amount is not None:
        expected_total = subtotal + tax_amount
        if abs(expected_total - total_amount) <= 1.0:
            arithmetic_check = "pass"
        else:
            arithmetic_check = "fail"
    else:
        arithmetic_check = "not_verifiable"

    confidence = data.get("confidence")
    flags = data.get("flags") or []

    needs_review = "Y" if (
        confidence == "low"
        or len(flags) > 0
        or arithmetic_check in ("fail", "not_verifiable")
    ) else "N"

    if arithmetic_check == "fail":
        message = (
            f"total does not match subtotal + tax "
            f"(expected {round(expected_total, 2)}, got {round(total_amount, 2)})"
        )
        if message not in flags:
            flags.append(message)
    elif arithmetic_check == "not_verifiable":
        message = "insufficient data for arithmetic check"
        if message not in flags:
            flags.append(message)

    data["flags"] = flags
    data["arithmetic_check"] = arithmetic_check
    data["needs_review"] = needs_review

    return data
