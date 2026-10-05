# File Transfer Integrity Verification using MD5 / SHA-256

A Computer Network Laboratory mini project that demonstrates how cryptographic hash functions can verify **data integrity** during file transfer over a TCP connection.

## Overview

The sender computes a hash (MD5 or SHA-256) of a file and transmits it along with the file. The receiver recomputes the hash on the data it actually received and compares the two values. A match means the file arrived intact; a mismatch means it was corrupted or tampered with in transit.

## Features

- TCP client–server file transfer using Python sockets
- Selectable hash algorithm: **MD5** or **SHA-256**
- Chunked reading/hashing, so large files don't need to fit in memory
- Integrity verdict displayed on both sender and receiver
- `--corrupt` option to simulate data corruption for demonstration

## Project Structure

```
.
├── server.py    # Receiver: saves file, recomputes hash, verifies
├── client.py    # Sender: hashes file, sends header + file
└── README.md
```

## Requirements

- Python 3.8+
- No external libraries (uses only `socket`, `hashlib`, `json`, `os`, `argparse`)

## Usage

**1. Start the receiver**

```bash
python server.py --port 5001 --out ./downloads
```

| Option   | Default   | Description                    |
|----------|-----------|--------------------------------|
| `--host` | `0.0.0.0` | Interface to listen on         |
| `--port` | `5001`    | Port number                    |
| `--out`  | `.`       | Directory for received files   |

**2. Send a file**

```bash
python client.py test.pdf --algo sha256
python client.py test.pdf --algo md5
```

| Option      | Default     | Description                                  |
|-------------|-------------|----------------------------------------------|
| `--host`    | `127.0.0.1` | Server IP address                            |
| `--port`    | `5001`      | Server port                                  |
| `--algo`    | `sha256`    | `md5` or `sha256`                            |
| `--corrupt` | off         | Flip one byte in transit to simulate tampering |

**3. Simulate corruption**

```bash
python client.py test.pdf --corrupt
```

## Sample Output

**Successful transfer**

```
# Server
File     : test.pdf (102400/102400 bytes)
Algorithm: SHA256
Sent hash: 9f86d081884c7d659a2feaa0c55ad015...
Calc hash: 9f86d081884c7d659a2feaa0c55ad015...
RESULT   : INTEGRITY VERIFIED ✔
```

**Corrupted transfer**

```
# Server
Sent hash: 9f86d081884c7d659a2feaa0c55ad015...
Calc hash: 3a7bd3e2360a3d29eea436fcfb7e44c7...
RESULT   : FILE CORRUPTED / TAMPERED ✘
```

*(Hash values above are illustrative.)*

## How It Works

```
 Sender                                   Receiver
   |  1. Compute hash of file               |
   |  2. Send header (name, size, algo, hash)|
   |--------------------------------------->|
   |  3. Send file bytes                    |
   |--------------------------------------->|
   |                 4. Recompute hash      |
   |                 5. Compare hashes      |
   |  6. OK / FAIL                          |
   |<---------------------------------------|
```

## MD5 vs SHA-256

| Property         | MD5                         | SHA-256                    |
|------------------|-----------------------------|----------------------------|
| Digest size      | 128 bits                    | 256 bits                   |
| Speed            | Faster                      | Slower                     |
| Collision resistance | Broken                  | Strong                     |
| Suitable for     | Detecting accidental errors | Integrity and security use |

## Limitations

- The hash is sent over the same channel as the file. An attacker who modifies the file in transit could also replace the hash. To defend against this, use **HMAC** with a shared secret or **digital signatures**.
- No encryption: file contents are sent in plaintext (TLS could be added).
- Handles one client connection at a time.

## Future Enhancements

- HMAC-SHA256 for authenticated integrity
- TLS/SSL for confidentiality
- Multi-client support using threads
- GUI and transfer progress bar

## License

This project is for educational purposes. Licensed under the MIT License.
