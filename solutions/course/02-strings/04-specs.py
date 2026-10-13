def money(price: float) -> str:
    return f"{price:,.2f}"


def receipt_total(price: float) -> str:
    amount = f"{price:,.2f}"
    label = "Total"
    message = f"{label}: {amount}"
    return message


def cents(price: float) -> str:
    text = f"{price:.2f}"
    return text


def receipt_name(name: str) -> str:
    return f"{name:>8}"
