import os

IP = '127.0.0.1'
PORT = 9090

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'db')        # User account data (one json file per user)
FILES_DIR = os.path.join(BASE_DIR, 'files')  # User drive files (one directory per user)
