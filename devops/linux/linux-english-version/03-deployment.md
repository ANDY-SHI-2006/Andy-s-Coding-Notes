[<- Prev: Linux advanced](02-linux-advanced.md)

# 3 Deployment

> This chapter turns your Django project into a real online service: web servers, Apache, MySQL, and the production combo **uWSGI + Nginx**.

## 3.1 Web Server Introduction

A **web server** is the backend server of a website; Django builds the web project on top of it.

| Server | Notes |
| --- | --- |
| **Apache** | The classic open-source web server, long ranked #1; simple, fast, stable, runs on almost any platform |
| **IIS** | Microsoft's web server |
| **Nginx** | Open-source newcomer from Russia; high concurrency, static-file & download server, load balancing, reverse proxy |
| **Tengine** | Taobao's fork of Nginx |

---

## 3.2 Setting up Apache

### Install

```bash
sudo apt update               # refresh package lists
sudo apt install apache2      # install Apache
```

### Manage the service

```bash
sudo systemctl start apache2     # start
sudo systemctl stop apache2      # stop
sudo systemctl status apache2    # check status
sudo systemctl restart apache2   # restart
sudo systemctl enable apache2    # start on boot
```

### Verify it's running

- `sudo systemctl status apache2` → look for `Active: active (running)`.
- In the VM browser: http://127.0.0.1 or http://localhost/
- From the physical machine: http://<vm-ip>

### Serve your own page

Put HTML files in `/var/www/html/`, e.g. `test.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Apache test passed</title>
</head>
<body>
    <h1>Hello, Apache!</h1>
    <h1 style="color: red">This means your Apache server is working!</h1>
</body>
</html>
```

---

## 3.3 Installing MySQL

```bash
sudo apt install mysql-server
```

### Security setup (interactive)

```bash
sudo mysql_secure_installation
# 1. Validate password strength        -> N (not needed while learning)
# 2. Remove anonymous users            -> Y
# 3. Disallow root remote login        -> N
# 4. Remove test database              -> Y
# 5. Reload privilege tables now       -> Y
```

### Set the root password

```bash
sudo mysql
```

```sql
use mysql;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;  -- reload the privilege tables
EXIT;              -- quit the MySQL shell
```

```bash
sudo systemctl restart mysql
mysql -uroot -p
```

### Allow remote access

```sql
use mysql;                               -- use the mysql database
update user set host="%" where user='root';  -- allow all hosts
FLUSH PRIVILEGES;
```

If a client (e.g. Navicat) still can't connect, edit the config:

```bash
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
# comment out this line with a leading #
# bind-address=127.0.0.1
sudo systemctl restart mysql
```

---

## 3.4 Deploying a Django Project

### Prepare the environment

```bash
sudo apt install python3
sudo apt install python3-pip
```

On Linux the commands change: `python` → `python3`, `pip` → `pip3`.

### Sync the environment

```bash
pip freeze > requirements.txt          # export (on the dev machine)
pip install -r requirements.txt        # install (on the server)
```

```bash
pip3 config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

pip3 install django==4.2.10

sudo apt install pkg-config            # mysql dev libraries
sudo apt install libmysqlclient-dev

pip3 install mysqlclient==2.1.1
pip3 install pillow
```

### Create the database and migrate

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### settings.py

```python
ALLOWED_HOSTS = ["*"]    # allow any host (NOT for production)
```

### Run locally

```bash
python3 manage.py runserver               # 127.0.0.1:8000 (local only)
python3 manage.py runserver 0.0.0.0:8000  # listen on all interfaces
```

> `runserver` is still **development mode** — it can't provide the concurrency, reliability, or security a real deployment needs.

### Configure a static IP (Netplan)

Edit `/etc/netplan/01-network-manager-all.yaml` (change `ens33`, IP, and gateway to match **your** network — do not copy blindly):

```yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    ens33:
      dhcp4: no
      addresses:
        - 192.168.16.66/24   # static IP + mask (24 = 255.255.255.0)
      gateway4: 192.168.16.2  # gateway
      nameservers:
          addresses: [114.114.114.114, 8.8.8.8]  # DNS servers
```

Apply and test:

```bash
sudo netplan apply
ifconfig               # check that ens33 changed
ping www.baidu.com     # test connectivity
```

---

## 3.5 uWSGI + Nginx Configuration

### Why uWSGI?

```text
Development:  browser -> Django (python manage.py runserver)   # local only
Production:   browser -> Nginx (web server) -> uWSGI (WSGI server) -> Django
```

The browser sends **HTTP**; Django understands **WSGI**. They don't speak the same protocol, so:

- **Nginx** accepts and returns HTTP (it does not understand WSGI).
- **uWSGI** sits between them and converts **HTTP ↔ WSGI** both ways.

| Point | Explanation |
| --- | --- |
| Protocol conversion | Nginx speaks HTTP, Django speaks WSGI, uWSGI translates between them |
| Production-ready | The built-in `runserver` is only for local debugging |
| Performance | uWSGI supports multiple workers, high concurrency, etc. |

### The request flow

1. Browser → Nginx on port 80/443 (HTTP).
2. Nginx routes: **static** requests (e.g. `/static/pic.png`) are served straight from disk; **dynamic** requests (e.g. `/api/...`) are forwarded to uWSGI.
3. uWSGI converts HTTP → WSGI and calls Django.
4. Django processes the logic and returns a WSGI response.
5. uWSGI converts WSGI → HTTP and returns it to Nginx.
6. Nginx returns the HTTP response to the browser.

### Install uWSGI

```bash
pip3 install uwsgi
sudo apt install uwsgi uwsgi-core uwsgi-plugin-python3
```

Create a `delop/` folder in the project, a `logs/` folder inside it, and a config file `uwsgi_conf.ini`:

```ini
[uwsgi]
# uwsgi IP and port (don't use 8000 - that's for Django's dev server)
socket=192.168.16.99:8001
# project root (adjust to yours)
chdir=/home/bb/code/bbs
# relative path to wsgi.py (adjust to yours)
wsgi-file=bbs/wsgi.py
# number of worker processes
processes=4
# number of threads
threads=2
# uwsgi role
master=True
# process id file (created automatically)
pidfile=uwsgi.pid
# log file (create the logs folder first)
daemonize=logs/uwsgi.log
# python environment path (check with: which python3)
pythonpath=/usr/bin/python3
```

Start / stop:

```bash
uwsgi --ini uwsgi_conf.ini    # start in the background
uwsgi --stop uwsgi.pid         # stop
ps -aux | grep uwsgi           # check if it's running
```

### Install and configure Nginx

```bash
sudo apt install nginx
```

Create `/etc/nginx/conf.d/nginx_conf.conf`:

```nginx
server {
    # listening port (HTTP default)
    listen 80;
    # domain or IP used for matching
    server_name 192.168.16.99;
    # default charset (avoid garbled Chinese)
    charset utf-8;
    # max upload size (default only 1MB)
    client_max_body_size 75M;
    # media files (user uploads) [optional]
    location /media {
        alias /home/bb/code/bbs/media/;
    }
    # static files (CSS, JS, images)
    location /static {
        alias /home/bb/code/bbs/static/;
    }
    # all other requests go to uwsgi
    location / {
        uwsgi_pass 192.168.16.99:8001;
        include /etc/nginx/uwsgi_params;
    }
}
```

Then edit `/etc/nginx/nginx.conf` and set the first line's user to your Linux username:

```bash
sudo vim /etc/nginx/nginx.conf
# user bb
```

Test and start:

```bash
sudo nginx -t -c /etc/nginx/nginx.conf   # test the config
sudo systemctl start nginx               # start
sudo systemctl status nginx              # check status
```

Visit http://192.168.203.66/ in the browser.

### Full startup / stop flow

```bash
# 1. start uwsgi (success = uwsgi.pid exists; check with ps -aux | grep uwsgi)
uwsgi --ini uwsgi_conf.ini
uwsgi --stop uwsgi.pid   # to stop

# 2. start nginx
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl status nginx
sudo systemctl restart nginx

# 3. visit the site - no port needed (nginx listens on 80 by default)
```

After changing Python code, restart uwsgi for it to take effect:

```bash
uwsgi --stop uwsgi.pid
uwsgi --ini uwsgi_conf.ini

# if stop says "pid not found", search and force kill
ps -aux | grep uwsgi
kill -9 PID
```

Reload Nginx config without a full restart:

```bash
sudo nginx -s reload -c /etc/nginx/nginx.conf
sudo systemctl reload nginx
# or fully restart
sudo systemctl restart nginx
```

Logs live in `delop/logs/uwsgi.log`.

---

| Do | Don't |
| --- | --- |
| Set a static IP (Netplan) before deploying | Don't copy the Netplan/YAML config blindly — match your network |
| Use `ALLOWED_HOSTS = ["*"]` only while learning | Don't leave `ALLOWED_HOSTS = ["*"]` in production |
| Restart uWSGI after changing Python code | Don't use `runserver` as your production server |
| Check `delop/logs/uwsgi.log` for errors | Don't run Apache and Nginx on the same port (80) together |

**Summary Mnemonic** — Nginx talks HTTP, Django talks WSGI, uWSGI translates between them; static → Nginx, dynamic → uWSGI → Django; install, then `systemctl start` + check `status` + visit the IP.

[<- Prev: Linux advanced](02-linux-advanced.md)
