import os

IP = '127.0.0.1'
PORT = 9090

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'db')        # 用户账号数据（每个用户一个 json 文件）
FILES_DIR = os.path.join(BASE_DIR, 'files')  # 用户网盘文件（每个用户一个目录）
