def format_currency(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0

    return f"₹ {value:,.2f}"


def format_percentage(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0

    return f"{value*100:.2f}%"


def truncate_hash(tx_hash):

    if not tx_hash:
        return "N/A"

    tx_hash = str(tx_hash)

    if len(tx_hash) < 16:
        return tx_hash

    return tx_hash[:10] + "..." + tx_hash[-6:]