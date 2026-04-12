from flask import Flask, request, render_template
import os
from core.crypto import sign_content, verify_content
from core.trust_engine import calculate_trust
from database.db import init_db, insert_file, get_all_files, get_file_by_name, get_file_by_id

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Database on startup
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sign", methods=["POST"])
def sign():
    file = request.files["file"]
    expiry = int(request.form["expiry"])

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # Output gives us metadata and signature
    output = sign_content(path, expiry)
    metadata = output["metadata"]
    
    # Store persistent record in the database
    insert_file(
        filename=file.filename,
        file_hash=metadata["hash"],
        expiry=metadata["expiry"],
        signature_hex=output["signature"]
    )

    return render_template("dashboard.html",
                           status="SIGNED",
                           score="100",
                           expiry=metadata["expiry"])


@app.route("/verify", methods=["POST"])
def verify():
    file = request.files["file"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    record = get_file_by_name(file.filename)
    if not record:
        return "Signature record not found in Database for file: " + file.filename, 404

    metadata = {
        "file": path,
        "hash": record["file_hash"],
        "expiry": record["expiry"]
    }

    result = verify_content(path, metadata, record["signature_hex"])
    score, status = calculate_trust(result)

    return render_template("dashboard.html",
                           status=status,
                           score=score,
                           expiry=result["expiry"])

@app.route("/registry")
def files():
    all_files = get_all_files()
    return render_template("files.html", files=all_files)

@app.route("/verify_record/<int:file_id>")
def verify_record(file_id):
    record = get_file_by_id(file_id)
    if not record:
        return "Signature record not found", 404
        
    path = os.path.join(UPLOAD_FOLDER, record["filename"])
    if not os.path.exists(path):
        return "Original file is missing from the server.", 404

    metadata = {
        "file": path,
        "hash": record["file_hash"],
        "expiry": record["expiry"]
    }

    result = verify_content(path, metadata, record["signature_hex"])
    score, status = calculate_trust(result)

    return render_template("dashboard.html",
                           status=status,
                           score=score,
                           expiry=result["expiry"])

if __name__ == "__main__":
    app.run(debug=True)
