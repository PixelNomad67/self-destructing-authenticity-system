import hashlib
import json
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature


def sign_content(file_path, expiry_seconds):
    with open(file_path, "rb") as f:
        content = f.read()

    content_hash = hashlib.sha256(content).hexdigest()

    expiry_time = (datetime.datetime.utcnow() +
                   datetime.timedelta(seconds=expiry_seconds)).isoformat()

    metadata = {
        "file": file_path,
        "hash": content_hash,
        "expiry": expiry_time
    }

    with open("keys/private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    signature = private_key.sign(
        json.dumps(metadata).encode(),
        ec.ECDSA(hashes.SHA256())
    )

    output = {
        "metadata": metadata,
        "signature": signature.hex()
    }

    return output


def verify_content(file_path, metadata, signature_hex):
    signature = bytes.fromhex(signature_hex)

    with open("keys/public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Expiry check
    expiry_time = datetime.datetime.fromisoformat(metadata["expiry"])
    expired = datetime.datetime.utcnow() > expiry_time

    # Hash check
    with open(file_path, "rb") as f:
        content = f.read()

    current_hash = hashlib.sha256(content).hexdigest()
    tampered = current_hash != metadata["hash"]

    # Signature check
    try:
        public_key.verify(
            signature,
            json.dumps(metadata).encode(),
            ec.ECDSA(hashes.SHA256())
        )
        signature_valid = True
    except InvalidSignature:
        signature_valid = False

    return {
        "expired": expired,
        "tampered": tampered,
        "signature_valid": signature_valid,
        "expiry": metadata["expiry"]
    }
