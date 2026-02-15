# Time-Bound Digital Authenticity System

## Overview

This project implements a time-scoped digital authenticity framework using cryptographic signatures and expiry enforcement.

Unlike traditional digital signatures that remain valid indefinitely, this system enforces a predefined authenticity window. After expiration, content is intentionally treated as untrusted.

## Motivation

Permanent authenticity can introduce risks such as replay attacks and misuse of outdated content. This system demonstrates lifecycle-based trust enforcement using:

- SHA-256 hashing
- ECDSA digital signatures
- Expiry-based policy validation

## Features

- Content hashing (SHA-256)
- Digital signature using ECDSA
- Time-bound authenticity window
- Tamper detection
- Expiry enforcement

## Project Structure

generate_keys.py → Generates ECDSA key pair
signer.py → Signs content with expiry metadata
verifier.py → Verifies integrity, signature, and expiry

## How It Works

1. Content is hashed.
2. Metadata includes hash and expiry timestamp.
3. Metadata is digitally signed.
4. Verification checks:
   - Integrity
   - Signature validity
   - Expiry status

Possible Outputs:
- VALID
- TAMPERED
- EXPIRED

## Installation

Install dependencies:

pip install -r requirements.txt

Generate keys:

python generate_keys.py

Sign content:

python signer.py content/sample.txt

Verify content:

python verifier.py

## Threat Model

This system protects against:
- Post-expiry replay of signed content
- Content tampering
- Unauthorized modification

It does not protect against:
- Full system compromise before expiry
- Advanced archival adversaries

## Future Work

- Automated key destruction
- Distributed key decay simulation
- Web-based verification interface

## Author

Piyush Roy 
Registration No.: 2427030318 
Section: C
