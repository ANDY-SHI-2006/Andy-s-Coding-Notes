import json
import os

from config.setting import DB_DIR, FILES_DIR
from utils import protocol


class ClientHandler:
    """处理单个客户端连接：注册、登录、查看、上传、下载。"""

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.username = None  # 登录后记录用户名

    def run(self):
        try:
            while True:
                raw = protocol.recv_msg(self.conn)
                if raw is None:
                    break  # 客户端断开连接
                request = json.loads(raw)
                handler = {
                    'reg': self.reg,
                    'login': self.login,
                    'ls': self.ls,
                    'upload': self.upload,
                    'download': self.download,
                }.get(request.get('cmd'))
                if handler is None:
                    self._reply(False, f"未知命令: {request.get('cmd')}")
                    continue
                handler(request)
        finally:
            self.conn.close()
            print(f'连接关闭: {self.addr}')

    # ---- 注册与登录 ----

    def reg(self, request):
        username = request['username']
        db_path = self._user_db_path(username)
        if os.path.exists(db_path):
            self._reply(False, f'用户 {username} 已存在')
            return
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump({'username': username, 'password': request['password']},
                      f, ensure_ascii=False)
        # 注册成功后在 files 下为该用户初始化网盘目录
        os.makedirs(os.path.join(FILES_DIR, username), exist_ok=True)
        self._reply(True, f'{username} 注册成功')

    def login(self, request):
        username = request['username']
        db_path = self._user_db_path(username)
        if not os.path.exists(db_path):
            self._reply(False, f'用户 {username} 不存在')
            return
        with open(db_path, encoding='utf-8') as f:
            record = json.load(f)
        if record['password'] != request['password']:
            self._reply(False, '密码错误')
            return
        self.username = username
        self._reply(True, '登录成功')

    # ---- 网盘操作 ----

    def ls(self, request):
        if not self._check_login():
            return
        target = self._user_files_dir()
        subdir = request.get('subdir')
        if subdir:
            target = os.path.join(target, subdir)
        if not os.path.isdir(target):
            self._reply(False, '目录不存在')
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
        self._reply(True, 'READY')  # 目录已准备好，通知客户端开始传文件
        ok = protocol.recv_file(self.conn, os.path.join(target_dir, filename))
        print(f"上传{'成功' if ok else '失败'}: {self.username}/{filename}")

    def download(self, request):
        if not self._check_login():
            return
        filename = os.path.basename(request['filename'])
        file_path = os.path.join(self._user_files_dir(), filename)
        if not os.path.isfile(file_path):
            self._reply(False, '文件不存在')
            return
        self._reply(True, 'READY')  # 文件存在，随后发送文件内容
        protocol.send_file(self.conn, file_path)
        print(f'下载完成: {self.username}/{filename}')

    # ---- 辅助方法 ----

    @staticmethod  # 不依赖实例状态，写成静态方法
    def _user_db_path(username):
        return os.path.join(DB_DIR, f'{username}.json')

    def _user_files_dir(self):
        return os.path.join(FILES_DIR, self.username)

    def _reply(self, ok, msg, **extra):
        payload = {'ok': ok, 'msg': msg}
        payload.update(extra)
        protocol.send_msg(self.conn, json.dumps(payload, ensure_ascii=False))

    def _check_login(self):
        if self.username is None:
            self._reply(False, '请先登录')
            return False
        return True
