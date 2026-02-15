import hashlib
import json
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature


# Load public key
with open("keys/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())


def verify_content():
    # Load signature file
    with open("metadata/signature.json", "r") as f:
        data = json.load(f)

    metadata = data["metadata"]
    signature = bytes.fromhex(data["signature"])

    file_path = metadata["file"]

    # Check expiry
    expiry_time = datetime.datetime.fromisoformat(metadata["expiry"])
    if datetime.datetime.utcnow() > expiry_time:
        print("STATUS: EXPIRED")
        return

    # Read file
    with open(file_path, "rb") as f:
        content = f.read()

    # Recalculate hash
    current_hash = hashlib.sha256(content).hexdigest()

    if current_hash != metadata["hash"]:
        print("STATUS: TAMPERED")
        return

    # Verify signature
    try:
        public_key.verify(
            signature,
            json.dumps(metadata).encode(),
            ec.ECDSA(hashes.SHA256())
        )
        print("STATUS: VALID")
    except InvalidSignature:
        print("STATUS: INVALID SIGNATURE")


if __name__ == "__main__":
    verify_content()

