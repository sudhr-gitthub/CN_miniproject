"""Sender: hashes a file (MD5 or SHA-256) and sends it with the hash to the server."""
import socket, hashlib, json, os, argparse

CHUNK = 4096

def file_hash(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=5001)
    p.add_argument("--algo", choices=["md5", "sha256"], default="sha256")
    p.add_argument("--corrupt", action="store_true",
                   help="flip a byte in transit to simulate corruption")
    a = p.parse_args()

    digest = file_hash(a.file, a.algo)
    header = {"filename": os.path.basename(a.file),
              "size": os.path.getsize(a.file),
              "algo": a.algo, "hash": digest}
    print(f"{a.algo.upper()} of original: {digest}")

    with socket.socket() as s:
        s.connect((a.host, a.port))
        s.sendall((json.dumps(header) + "\n").encode())
        first = True
        with open(a.file, "rb") as f:
            while chunk := f.read(CHUNK):
                if a.corrupt and first:
                    chunk = bytes([chunk[0] ^ 0xFF]) + chunk[1:]
                    print("!! Simulating corruption of first byte")
                first = False
                s.sendall(chunk)
        reply = s.recv(16).decode().strip()

    print("Server verdict:", "INTEGRITY VERIFIED ✔" if reply == "OK"
          else "CORRUPTED ✘")

if __name__ == "__main__":
    main()
