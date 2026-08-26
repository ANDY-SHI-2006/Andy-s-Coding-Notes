[← Previous: HTTP and a Simple Web Server](04-http-and-a-simple-web-server.md)

# 5. Project: A Simple Network Drive

This chapter combines everything from the previous four chapters into one complete project: a simple network drive (netdisk) system over TCP. After registering and logging in, users can list, upload, and download files in their own drive directory. The project uses the socket API from Chapter 2, the length-prefix protocol from Chapter 3, and object-oriented code organization.

## 5.1 Project Design

### 5.1.1 Requirements

**Client:**

- `reg`: register; the server creates a dedicated drive directory for the new user
- `login`: log in; all drive operations require being logged in
- `ls`: list files in the drive directory (optionally a first-level subdirectory)
- `upload`: upload a local file to the drive (overwrites if it already exists)
- `download`: download a file from the drive to the local machine
- `exit`: quit

**Server:**

- Registration and login; account data stored in `db/` (one JSON file per user)
- List, upload, and download; files stored under `files/<username>/`
- Multiple clients at the same time

### 5.1.2 Directory Layout

```
netdisk/
├── server/                  # Server side
│   ├── main.py              # Entry point
│   ├── config/setting.py    # IP, port, data directories
│   ├── core/server.py       # Socket listening and connection management
│   ├── core/handler.py      # Business logic: reg, login, ls, upload, download
│   ├── utils/protocol.py    # Wire protocol: message and file transfer
│   ├── db/                  # Created at runtime: user account data
│   └── files/               # Created at runtime: user drive files
└── client/                  # Client side
    ├── main.py              # Entry point
    ├── config/setting.py    # Server address, download directory
    ├── core/client.py       # Connection setup
    ├── core/handler.py      # Interactive menu and command parsing
    ├── utils/protocol.py    # Same protocol implementation as the server
    └── downloads/           # Created at runtime: downloaded files
```

`db/` and `files/` are created automatically when the server starts; `downloads/` is created by the client on the first download. No manual setup is needed.

Complete runnable project: [server](../examples/en/netdisk/server/main.py) · [client](../examples/en/netdisk/client/main.py) (run `python main.py` in the `server/` and `client/` directories respectively)

### 5.1.3 Protocol Design

The protocol reuses the **length-prefix scheme** from Chapter 3 (4-byte header in `struct`'s `!I` network byte order, plus an exact-read loop), with two conventions:

1. **Control messages are JSON**: the client sends `{"cmd": "login", "username": "...", "password": "..."}` and the server replies `{"ok": true, "msg": "..."}`. Compared with space-separated strings, JSON is immune to filenames containing spaces, and the field meanings are self-evident.
2. **File transfer is two-phase**: for `upload`, the client first sends the `upload` command (JSON); the server confirms the directory is ready and replies `READY`; only then does the client send the file content (4-byte file size + chunked data).

## 5.2 The Shared Protocol Module

`utils/protocol.py` is identical on the client and the server — it is the foundation of the whole project (full code: [utils/protocol.py](../examples/en/netdisk/server/utils/protocol.py); the client's file with the same name is identical):

```python
# utils/protocol.py
import os
import struct

HEADER_FORMAT = '!I'  # Unsigned 4-byte integer in network byte order (see Chapter 3)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CHUNK_SIZE = 4096


def _recv_exactly(sock, size):
    """Loop until exactly size bytes are read; return None if the peer disconnects."""
    chunks = bytearray()
    while len(chunks) < size:
        chunk = sock.recv(size - len(chunks))
        if not chunk:
            return None
        chunks.extend(chunk)
    return bytes(chunks)


def send_msg(sock, message):
    """Send a text message with a 4-byte length header prepended."""
    data = message.encode('utf-8')
    sock.sendall(struct.pack(HEADER_FORMAT, len(data)))
    sock.sendall(data)


def recv_msg(sock):
    """Receive a text message; return None if the peer disconnects."""
    header = _recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return None
    length = struct.unpack(HEADER_FORMAT, header)[0]
    data = _recv_exactly(sock, length)
    if data is None:
        return None
    return data.decode('utf-8')


def send_file(sock, file_path):
    """Send the 4-byte file size first, then the file content in chunks."""
    size = os.path.getsize(file_path)
    sock.sendall(struct.pack(HEADER_FORMAT, size))
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sock.sendall(chunk)


def recv_file(sock, file_path):
    """Receive the 4-byte file size, then read chunks into file_path. Returns True on success."""
    header = _recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return False
    size = struct.unpack(HEADER_FORMAT, header)[0]
    received = 0
    with open(file_path, 'wb') as f:
        while received < size:
            chunk = sock.recv(min(CHUNK_SIZE, size - received))
            if not chunk:
                return False
            f.write(chunk)
            received += len(chunk)
    return True
```

Like message transfer, `send_file` / `recv_file` send the 4-byte file size first and then move data in `CHUNK_SIZE` blocks — exactly the "read the header, then read precisely that many bytes" pattern from Section 3.1.

## 5.3 Server Implementation

### 5.3.1 Listening and Multiple Clients

The server's main loop is short: each accepted connection goes to a `ClientHandler` running on its own thread, so multiple clients can use the drive at the same time.

```python
# core/server.py
import os
import socket
import threading

from config.setting import DB_DIR, FILES_DIR, IP, PORT
from core.handler import ClientHandler


class Server:
    def __init__(self):
        # Make sure the data directories exist at startup
        os.makedirs(DB_DIR, exist_ok=True)
        os.makedirs(FILES_DIR, exist_ok=True)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, PORT))
        sock.listen(5)
        print(f'Netdisk server listening on {IP}:{PORT}')
        while True:
            conn, addr = sock.accept()
            print(f'New connection: {addr}')
            # One thread per connection, so multiple clients can use the drive at once
            handler = ClientHandler(conn, addr)
            threading.Thread(target=handler.run, daemon=True).start()
```

Full code: [core/server.py](../examples/en/netdisk/server/core/server.py)

> File transfer is a stateful, multi-step process ("command + several receives"). In the single-threaded `select` model from 3.3, one client transferring a large file would stall everyone else. One thread per connection is the simplest workable concurrency scheme here; larger production systems would use a thread pool or `asyncio`.

### 5.3.2 Command Dispatch and Account Management

`ClientHandler.run` loops over JSON commands and dispatches them to methods. Registration writes the account to `db/<username>.json` and initializes the drive directory; login verifies the password and records the current user:

```python
# core/handler.py (excerpt)
class ClientHandler:
    """Handle a single client connection: register, login, ls, upload, download."""

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.username = None  # Recorded after login

    def run(self):
        try:
            while True:
                raw = protocol.recv_msg(self.conn)
                if raw is None:
                    break  # Client disconnected
                request = json.loads(raw)
                handler = {
                    'reg': self.reg,
                    'login': self.login,
                    'ls': self.ls,
                    'upload': self.upload,
                    'download': self.download,
                }.get(request.get('cmd'))
                if handler is None:
                    self._reply(False, f"Unknown command: {request.get('cmd')}")
                    continue
                handler(request)
        finally:
            self.conn.close()

    def reg(self, request):
        username = request['username']
        db_path = self._user_db_path(username)
        if os.path.exists(db_path):
            self._reply(False, f'User {username} already exists')
            return
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump({'username': username, 'password': request['password']},
                      f, ensure_ascii=False)
        # Initialize the user's drive directory under files/
        os.makedirs(os.path.join(FILES_DIR, username), exist_ok=True)
        self._reply(True, f'{username} registered')
```

Full code: [core/handler.py](../examples/en/netdisk/server/core/handler.py)

Dispatching through a dictionary (`{'reg': self.reg, ...}`) beats a long `if/elif` chain: adding a command only takes one new method and one dictionary entry.

`exit` is not in the dispatch table: the client handles it locally by closing the connection and quitting; the server notices through `recv_msg` returning `None`.

### 5.3.3 Upload and Download

Upload and download are both two-phase flows: confirm first, then transfer. Upload, for example:

```python
# core/handler.py (excerpt)
    def upload(self, request):
        if not self._check_login():
            return
        filename = os.path.basename(request['filename'])
        target_dir = self._user_files_dir()
        subdir = request.get('subdir')
        if subdir:
            target_dir = os.path.join(target_dir, subdir)
            os.makedirs(target_dir, exist_ok=True)
        self._reply(True, 'READY')  # Directory ready; tell the client to start sending
        ok = protocol.recv_file(self.conn, os.path.join(target_dir, filename))
        print(f"Upload {'succeeded' if ok else 'failed'}: {self.username}/{filename}")
```

Full code: [core/handler.py](../examples/en/netdisk/server/core/handler.py) (same file as 5.3.2)

`download` mirrors it: the server confirms the file exists, replies `READY`, then calls `send_file`. Note that `os.path.basename` strips any directory components from the client-supplied name, keeping only the final segment.

## 5.4 Client Implementation

The client prints the menu, parses input, and sends commands. Every command method follows the same pattern: validate arguments → `_request` sends JSON and returns the response → act on the `ok` field:

```python
# core/handler.py (excerpt)
    def upload(self, *args):
        if len(args) not in (1, 2):
            print('Usage: upload <local-path> [drive-subdir]')
            return
        local_path = args[0]
        if not os.path.isfile(local_path):
            print('Local file does not exist')
            return
        request = {'cmd': 'upload', 'filename': os.path.basename(local_path)}
        if len(args) == 2:
            request['subdir'] = args[1]
        resp = self._request(request)
        if not resp['ok']:
            print(resp['msg'])
            return
        protocol.send_file(self.sock, local_path)  # Server is ready; send the content
        print('Upload finished')

    def _request(self, payload):
        """Send a JSON command and return the parsed JSON response."""
        protocol.send_msg(self.sock, json.dumps(payload, ensure_ascii=False))
        return json.loads(protocol.recv_msg(self.sock))
```

Full code: [core/handler.py](../examples/en/netdisk/client/core/handler.py)

## 5.5 Running the Demo

Start the server first, then the client (each in its own directory). The demo's `upload` needs a local file: create `notes.txt` with a few lines of content in the `client/` directory first:

```bash
cd examples/en/netdisk/server && python main.py
# Netdisk server listening on 127.0.0.1:9090

cd examples/en/netdisk/client && python main.py
```

A full client session:

```
>>> reg tom 123
tom registered
>>> login tom 123
Login successful
>>> upload notes.txt
Upload finished
>>> upload notes.txt study
Upload finished
>>> ls
  notes.txt
  study
>>> ls study
  notes.txt
>>> download notes.txt
Download finished: .../client/downloads/notes.txt
>>> exit
```

## 5.6 Limitations

This implementation optimizes for teaching clarity; a real network drive would go much further:

- **Plaintext passwords**: a real system stores hashes (e.g. `hashlib.pbkdf2_hmac`), never plaintext.
- **No transfer integrity check**: add an MD5/SHA checksum to confirm the file arrived intact.
- **Large files and resume**: the 4-byte size field caps files at ~4 GB, and an interrupted transfer must restart from scratch.
- **Path safety**: the `ls` subdirectory argument does not defend against `..`; strict deployments should verify paths stay inside the user's directory.
> **Summary**: This project introduces no new knowledge — its value is in combination. Socket connections, the length-prefix protocol, JSON messages, file IO, and object-oriented dispatch each come from earlier chapters. If you can read and reproduce this project on your own, the course has done its job.

[← Previous: HTTP and a Simple Web Server](04-http-and-a-simple-web-server.md) | [Back to networking basics](README.md)
