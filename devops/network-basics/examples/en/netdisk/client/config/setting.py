import os

IP = '127.0.0.1'
PORT = 9090

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')  # Where downloaded files are saved
