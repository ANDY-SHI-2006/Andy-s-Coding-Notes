import json
import os

from config.setting import DB_DIR, FILES_DIR
from utils import protocol


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
            print(f'Connection closed: {self.addr}')

    # ---- Register & login ----

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

    def login(self, request):
        username = request['username']
        db_path = self._user_db_path(username)
        if not os.path.exists(db_path):
            self._reply(False, f'User {username} does not exist')
            return
        with open(db_path, encoding='utf-8') as f:
            record = json.load(f)
        if record['password'] != request['password']:
            self._reply(False, 'Wrong password')
            return
        self.username = username
        self._reply(True, 'Login successful')

    # ---- Drive operations ----

    def ls(self, request):
        if not self._check_login():
            return
        target = self._user_files_dir()
        subdir = request.get('subdir')
        if subdir:
            target = os.path.join(target, subdir)
        if not os.path.isdir(target):
            self._reply(False, 'Directory does not exist')
            return
        self._reply(True, 'OK', items=sorted(os.listdir(target)))

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

    def download(self, request):
        if not self._check_login():
            return
        filename = os.path.basename(request['filename'])
        file_path = os.path.join(self._user_files_dir(), filename)
        if not os.path.isfile(file_path):
            self._reply(False, 'File does not exist')
            return
        self._reply(True, 'READY')  # File exists; content follows
        protocol.send_file(self.conn, file_path)
        print(f'Download finished: {self.username}/{filename}')

    # ---- Helpers ----

    def _user_db_path(self, username):
        return os.path.join(DB_DIR, f'{username}.json')

    def _user_files_dir(self):
        return os.path.join(FILES_DIR, self.username)

    def _reply(self, ok, msg, **extra):
        payload = {'ok': ok, 'msg': msg}
        payload.update(extra)
        protocol.send_msg(self.conn, json.dumps(payload, ensure_ascii=False))

    def _check_login(self):
        if self.username is None:
            self._reply(False, 'Please log in first')
            return False
        return True
