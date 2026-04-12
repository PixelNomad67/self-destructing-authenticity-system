import hashlib
import json
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

def verify_content(file_path):
    with open("metadata/signature.json", "r") as f:
        data = json.load(f)

    metadata = data["metadata"]
    signature = bytes.fromhex(data["signature"])

    with open("keys/public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Expiry check
    expiry_time = datetime.datetime.fromisoformat(metadata["expiry"])
    if datetime.datetime.utcnow() > expiry_time:
        return "EXPIRED"

    # Hash check
    with open(file_path, "rb") as f:
        content = f.read()

    current_hash = hashlib.sha256(content).hexdigest()

    if current_hash != metadata["hash"]:
        return "TAMPERED"

    # Signature check
    try:
        public_key.verify(
            signature,
            json.dumps(metadata).encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return "VALID"
    except InvalidSignature:
        return "INVALID SIGNATURE"
