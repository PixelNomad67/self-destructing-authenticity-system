import hashlib
import json
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature


# Load private key
with open("keys/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)


def sign_content(file_path, expiry_seconds=60):
    # Read file
    with open(file_path, "rb") as f:
        content = f.read()

    # Hash content
    content_hash = hashlib.sha256(content).hexdigest()

    # Set expiry
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry_seconds)
    expiry_str = expiry_time.isoformat()

    # Metadata
    metadata = {
        "file": file_path,
        "hash": content_hash,
        "expiry": expiry_str
    }

    metadata_bytes = json.dumps(metadata).encode()

    # Sign metadata
    signature = private_key.sign(
        metadata_bytes,
        ec.ECDSA(hashes.SHA256())
    )

    # Save metadata + signature
    output = {
        "metadata": metadata,
        "signature": signature.hex()
    }

    with open("metadata/signature.json", "w") as f:
        json.dump(output, f, indent=4)

    print("Content signed successfully.")
    print("Expires at:", expiry_str)


if __name__ == "__main__":
    sign_content("content/sample.txt", expiry_seconds=60)

