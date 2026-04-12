import datetime

def calculate_trust(result):
    if result["tampered"]:
        return 0, "TAMPERED"

    if not result["signature_valid"]:
        return 10, "INVALID SIGNATURE"

    expiry_time = datetime.datetime.fromisoformat(result["expiry"])
    remaining = (expiry_time - datetime.datetime.utcnow()).total_seconds()

    if result["expired"]:
        return 20, "EXPIRED"

    if remaining < 30:
        return 60, "NEAR EXPIRY"

    return 90, "VALID"
