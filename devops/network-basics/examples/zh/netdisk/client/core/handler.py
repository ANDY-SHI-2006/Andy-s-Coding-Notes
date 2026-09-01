import json
import os

from config.setting import DOWNLOAD_DIR
from utils import protocol

MENU = '''
======== 简易网盘 ========
  reg <用户名> <密码>             注册
  login <用户名> <密码>           登录
  ls [子目录]                     查看网盘文件
  upload <本地路径> [网盘子目录]  上传文件
  download <文件名>               下载文件
  passwd <新密码>                 修改密码
  info                            查看账号信息
  logout                          退出登录
  exit                            退出
========================='''


class PanClient:
    """客户端交互：解析用户输入，向服务端发送命令并处理响应。"""

    def __init__(self, sock):
        self.sock = sock
        self.username = None

    def run(self):
        while True:
            print(MENU)
            print('当前用户:', self.username or '未登录')
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
                'passwd': self.passwd,
                'info': self.info,
                'logout': self.logout,
            }.get(cmd)
            if action is None:
                print('未知命令')
                continue
            action(*args)

    # ---- 命令 ----

    def reg(self, *args):
        if len(args) != 2:
            print('格式: reg <用户名> <密码>')
            return
        resp = self._request({'cmd': 'reg', 'username': args[0], 'password': args[1]})
        print(resp['msg'])

    def login(self, *args):
        if len(args) != 2:
            print('格式: login <用户名> <密码>')
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
            print('格式: upload <本地路径> [网盘子目录]')
            return
        local_path = args[0]
        if not os.path.isfile(local_path):
            print('本地文件不存在')
            return
        request = {'cmd': 'upload', 'filename': os.path.basename(local_path)}
        if len(args) == 2:
            request['subdir'] = args[1]
        resp = self._request(request)
        if not resp['ok']:
            print(resp['msg'])
            return
        protocol.send_file(self.sock, local_path)  # 服务端就绪后发送文件内容
        print('上传完成')

    def download(self, *args):
        if len(args) != 1:
            print('格式: download <文件名>')
            return
        resp = self._request({'cmd': 'download', 'filename': args[0]})
        if not resp['ok']:
            print(resp['msg'])
            return
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        # 只取文件名部分，防止输入包含路径时写到 downloads 目录之外
        save_path = os.path.join(DOWNLOAD_DIR, os.path.basename(args[0]))
        protocol.recv_file(self.sock, save_path)
        print(f'下载完成: {save_path}')

    def passwd(self, *args):
        if len(args) != 1:
            print('格式: passwd <新密码>')
            return
        resp = self._request({'cmd': 'passwd', 'password': args[0]})
        print(resp['msg'])

    def info(self, *args):
        if args:
            print('格式: info')
            return
        resp = self._request({'cmd': 'info'})
        if not resp['ok']:
            print(resp['msg'])
            return
        print(f"注册时间: {resp['create_time']}")
        print(f"文件数量: {resp['file_count']}")
        print(f"占用空间: {resp['total_size'] / 1024:.1f} KB")

    def logout(self, *args):
        if args:
            print('格式: logout')
            return
        resp = self._request({'cmd': 'logout'})
        print(resp['msg'])
        if resp['ok']:
            self.username = None

    # ---- 辅助方法 ----

    def _request(self, payload):
        """发送一个 JSON 命令，并返回解析后的 JSON 响应。"""
        protocol.send_msg(self.sock, json.dumps(payload, ensure_ascii=False))
        return json.loads(protocol.recv_msg(self.sock))
