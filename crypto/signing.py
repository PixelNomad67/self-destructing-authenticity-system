import hashlib
import json
import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

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

    with open("metadata/signature.json", "w") as f:
        json.dump(output, f, indent=4)

    return expiry_time
