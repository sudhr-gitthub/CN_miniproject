"""Receiver: accepts a file, recomputes its hash, compares with the sender's hash."""
import socket, hashlib, json, os, argparse

CHUNK = 4096

def recv_line(conn):
    data = b""
    while not data.endswith(b"\n"):
        b = conn.recv(1)
        if not b:
            break
        data += b
    return data.decode().strip()

def handle(conn, outdir):
    header = json.loads(recv_line(conn))
    name = os.path.basename(header["filename"])
    size, algo, sent_hash = header["size"], header["algo"], header["hash"]
    h = hashlib.new(algo)
    path = os.path.join(outdir, "received_" + name)

    received = 0
    with open(path, "wb") as f:
        while received < size:
            chunk = conn.recv(min(CHUNK, size - received))
            if not chunk:
                break
            f.write(chunk)
            h.update(chunk)
            received += len(chunk)

    calc = h.hexdigest()
    print(f"File     : {name} ({received}/{size} bytes)")
    print(f"Algorithm: {algo.upper()}")
    print(f"Sent hash: {sent_hash}")
    print(f"Calc hash: {calc}")
    if calc == sent_hash and received == size:
        print("RESULT   : INTEGRITY VERIFIED ✔\n")
        conn.sendall(b"OK\n")
    else:
        print("RESULT   : FILE CORRUPTED / TAMPERED ✘\n")
        conn.sendall(b"FAIL\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=5001)
    p.add_argument("--out", default=".")
    a = p.parse_args()

    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((a.host, a.port))
        s.listen(5)
        print(f"Server listening on {a.host}:{a.port}")
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            with conn:
                handle(conn, a.out)

if __name__ == "__main__":
    main()
