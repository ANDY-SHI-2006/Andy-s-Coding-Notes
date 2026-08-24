import json
import os

from config.setting import DOWNLOAD_DIR
from utils import protocol

MENU = '''
======== Simple Netdisk ========
  reg <username> <password>          Register
  login <username> <password>        Log in
  ls [subdir]                        List drive files
  upload <local-path> [drive-subdir] Upload a file
  download <filename>                Download a file
  exit                               Quit
================================='''


class PanClient:
    """Client interaction: parse user input, send commands, handle responses."""

    def __init__(self, sock):
        self.sock = sock
        self.username = None

    def run(self):
        while True:
            print(MENU)
            print('Current user:', self.username or 'not logged in')
            parts = input('>>> ').split()
            if not parts:
                continue
            cmd, args = parts[0], parts[1:]
            if cmd == 'exit':
                break
            action = {
                'reg': self.reg,
                'login': self.login,
                'ls': self.ls,
                'upload': self.upload,
                'download': self.download,
            }.get(cmd)
            if action is None:
                print('Unknown command')
                continue
            action(*args)

    # ---- Commands ----

    def reg(self, *args):
        if len(args) != 2:
            print('Usage: reg <username> <password>')
            return
        resp = self._request({'cmd': 'reg', 'username': args[0], 'password': args[1]})
        print(resp['msg'])

    def login(self, *args):
        if len(args) != 2:
            print('Usage: login <username> <password>')
            return
        resp = self._request({'cmd': 'login', 'username': args[0], 'password': args[1]})
        print(resp['msg'])
        if resp['ok']:
            self.username = args[0]

    def ls(self, *args):
        request = {'cmd': 'ls'}
        if len(args) == 1:
            request['subdir'] = args[0]
        resp = self._request(request)
        if resp['ok']:
            for item in resp['items']:
                print(' ', item)
        else:
            print(resp['msg'])

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

    def download(self, *args):
        if len(args) != 1:
            print('Usage: download <filename>')
            return
        resp = self._request({'cmd': 'download', 'filename': args[0]})
        if not resp['ok']:
            print(resp['msg'])
            return
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        save_path = os.path.join(DOWNLOAD_DIR, args[0])
        protocol.recv_file(self.sock, save_path)
        print(f'Download finished: {save_path}')

    # ---- Helpers ----

    def _request(self, payload):
        """Send a JSON command and return the parsed JSON response."""
        protocol.send_msg(self.sock, json.dumps(payload, ensure_ascii=False))
        return json.loads(protocol.recv_msg(self.sock))
