---
title: Epoch Seal
emoji: 🛡️
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
app_port: 7860
---

# 🛡️ EpochSeal: Time-Bound Digital Authenticity System

[![Live Demo](https://img.shields.io/badge/Live_Demo-Hugging_Face-indigo?style=for-the-badge&logo=huggingface)](https://p-yuxh-self-destructing-authenticity-system.hf.space)

**EpochSeal** is a groundbreaking framework that introduces expiration dates to digital authenticity. Unlike traditional digital signatures that remain valid indefinitely (potentially leading to replay attacks or out-of-context misuse), this system ensures that signed content is only considered authentic within a predefined, strict time window. Once the time is up, the content safely "self-destructs" its trusted status.

---

## ✨ Features

- **⏳ Time-Bound Authenticity**: Cryptographically enforce an expiration timestamp on files.
- **🔒 Secure ECDSA Signatures**: Bulletproof authenticity validation using Elliptic Curve Digital Signature Algorithm.
- **🛡️ Tamper Detection**: Instant integrity validation using SHA-256 hashing.
- **🗃️ Persistent Registry**: SQLite-backed record management for historical tracking of signed credentials.
- **🌐 Web Interface**: Clean, dark-mode, glassmorphic UI built with Flask to easily sign and verify files. 

---

## 🚀 Live Demo

You can try the fully functioning web application directly in your browser:
👉 **[Launch EpochSeal on Hugging Face](https://p-yuxh-self-destructing-authenticity-system.hf.space)** (Direct Full-Screen Link)
<br>
👉 **[Hugging Face Space Repository](https://huggingface.co/spaces/p-yuxh/self-destructing-authenticity-system)** 

---

## 🛠️ How It Works

1. **Upload & Hash**: An uploaded file is hashed using **SHA-256**.
2. **Metadata Generation**: The hash, along with a specified **expiry timestamp**, is packaged into a metadata object.
3. **Cryptographic Signing**: The metadata is digested and signed using the server's private ECDSA key.
4. **Verification Flow**: 
   - When verified, the system recalculates the hash and parses the original signature.
   - It checks the validity of the signature, ensures the file has not been tampered with, and validates if the current time is earlier than the expiry time.
   - **Outputs** resulting status: `VALID` (100 Trust Score), `TAMPERED` (0 Trust Score), or `EXPIRED` (0 Trust Score).

---

## 💻 Local Installation

To run EpochSeal on your own machine:

### 1. Clone & Set Up
```bash
# Clone your repository (update with your actual git repo)
git clone ...
cd self-destructing-authenticity-system

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Cryptographic Keys
Before the first run, ensure cryptographic keys are populated:
```bash
python generate_keys.py
```

### 3. Run the Web Server
Launch the Flask dashboard locally:
```bash
python app.py
```
Then, open your browser and navigate to `http://127.0.0.1:5000`.

*(Note: Command-line testing is also available via `signer.py` and `verifier.py`)*

---

## 🛡️ Threat Model

**Mitigates:**
- Post-expiry replay of signed content
- Content tampering and unauthorized modification

**Out of Scope:**
- Full system compromise prior to file expiry
- Extremely advanced archival adversaries storing states before expiry

---

## 🔮 Future Work

- [ ] Automated cryptographic key destruction
- [ ] Distributed key decay simulation
- [ ] Decentralized verification networks

---

## 👨‍💻 Author
**Piyush Roy**  
Registration No.: `2427030318`  
Section: `C`
