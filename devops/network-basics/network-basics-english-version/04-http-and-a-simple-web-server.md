[← Previous: Sticky Packets and Concurrency](03-sticky-packets-and-concurrency.md)

# 4. HTTP and a Simple Web Server

This chapter pushes the TCP socket knowledge from earlier chapters one level up: we hand-roll a web server that a browser can talk to. For HTTP protocol details (methods, status codes, caching, HTTPS), see [Section 1.4](01-networking-fundamentals.md); the focus here is turning the protocol format into a running server.

## 4.1 From Socket to Web Server

### 4.1.1 The Browser Is the Client

In the B/S architecture (see 1.1.2), the browser acts as the client: typing `127.0.0.1:8000` into the address bar makes the browser open a TCP connection to port 8000 and send an HTTP request. So an ordinary TCP server only needs a small makeover to "become" a web server.

### 4.1.2 Minimal Attempt: Reply with a Plain Sentence

Start with the plain TCP server from Chapter 2, replying with an arbitrary sentence:

Complete runnable example: [the invalid-response control experiment](../examples/en/http_server_naive.py)

```python
# http_server_naive.py
import socket

# Create the most basic TCP server (socket() with no arguments defaults to IPv4 + TCP)
sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    # Read and print the browser's raw HTTP request
    headers = conn.recv(1024).decode()
    print(headers)
    # Deliberately reply with content that is NOT a valid HTTP response, to observe the browser's reaction
    conn.send(b'hello world')
    conn.close()
```

Visit `http://127.0.0.1:8000` in a browser. The terminal prints the browser's raw request, but the browser usually shows an error or garbled output — because `hello world` does not follow the HTTP response format, and the browser does not know how to parse it. This server is a deliberately "invalid" control experiment for observing how browsers behave when faced with a malformed response.

In practice, Chrome flat-out reports `ERR_INVALID_HTTP_RESPONSE` ("sent an invalid response"):

![[browser-invalid-http-response.png|700]]

## 4.2 What the Browser's Request Looks Like

The printed content looks roughly like this:

```http
GET / HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 ...
Accept: text/html,application/xhtml+xml,...
Accept-Language: en-US,en;q=0.9
Connection: keep-alive

```

An HTTP request has four parts (details in 1.4.1):

1. **Request line**: method + path + protocol version, e.g. `GET /index HTTP/1.1`.
2. **Headers**: several `Key: Value` lines, each ending with `\r\n`.
3. **Empty line**: a lone `\r\n` marking the end of the headers.
4. **Body** (optional): GET/HEAD usually have no body; POST/PUT carry submitted data.

> Tip: browsers usually send an extra request for `/favicon.ico` (the site icon). Don't be surprised to see it in the logs.

## 4.3 Returning a Valid HTTP Response

An HTTP response also has four parts:

1. **Status line**: protocol version + status code + reason phrase, e.g. `HTTP/1.1 200 OK`.
2. **Headers**: `Key: Value` lines; at minimum, `Content-Type` tells the browser what the body is.
3. **Empty line**: `\r\n`, marking the end of the headers.
4. **Body**: the content the browser actually renders.

As long as the reply follows this format, the browser renders it correctly:

Complete runnable example: [minimal web server](../examples/en/http_server_minimal.py)

```python
# http_server_minimal.py
import socket

# 1. Create a TCP socket, bind the address, and start listening (SO_REUSEADDR allows port reuse after restarts)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    # 2. Accept a browser connection and read the request
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request.split('\r\n')[0])  # Print only the request line, e.g. GET / HTTP/1.1

    # 3. Reply in HTTP response format: status line + headers + empty line + body
    conn.sendall(b'HTTP/1.1 200 OK\r\n')
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')  # The empty line marks the end of the response headers
    conn.sendall('<h1>Hello, world</h1>'.encode('utf-8'))
    conn.close()
```

Run it and visit `http://127.0.0.1:8000` in a browser — the page shows a big "Hello, world".

Screenshot of an actual run:

![[http-server-browser-hello.png]]

**What you'll see**: the terminal prints the request line of each request (browsers usually also fire a `/favicon.ico` request):

```
GET / HTTP/1.1
GET /favicon.ico HTTP/1.1
```

Screenshot of an actual run (after visiting `/`, the browser automatically requests `/favicon.ico`):

![[http-server-terminal-requests.png]]

If you don't want to open a browser, curl shows the raw response including the status line and headers (more HTTP testing tools in 1.5.5):

```bash
curl -i http://127.0.0.1:8000/
# HTTP/1.1 200 OK
# Content-Type: text/html; charset=utf-8
#
# <h1>Hello, world</h1>
```

> Including `charset=utf-8` in `Content-Type` avoids mojibake for non-ASCII text.

## 4.4 Parsing the Path and Simple Routing

When the browser visits different addresses (e.g. `/index`, `/cart`), the only difference is the second field of the request line. Parse the path out, and you can return different content per path — the embryonic form of "routing" in web frameworks:

Complete runnable example: [web server with routing](../examples/en/http_server_routing.py)

```python
# http_server_routing.py
import socket

# 1. Create a TCP socket, bind the address, and start listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()

    # 2. Parse the path: the request line looks like "GET /cart HTTP/1.1"; split out the second field
    request_line = request.split('\r\n')[0]
    path = request_line.split(' ')[1]
    print(f"Request path: {path}")

    # 3. Choose the status code and body based on the path (the embryonic form of routing)
    if path == '/index':
        status, body = '200 OK', '<h1>Home</h1>'
    elif path == '/cart':
        status, body = '200 OK', '<h1>Shopping cart</h1>'
    else:
        status, body = '404 Not Found', '<h1>404 Not Found</h1>'

    # 4. Reply in HTTP response format: status line + headers + empty line + body
    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
```

Visiting `http://127.0.0.1:8000/index` and `http://127.0.0.1:8000/cart` shows different pages; any other path returns a 404 page.

Screenshots of an actual run — `/index` and `/cart` each return a different page:

![[http-routing-browser-index.png]]

![[http-routing-browser-cart.png]]

**What you'll see**: the terminal prints the path parsed from each request (note that `/favicon.ico` falls into the 404 branch too):

```
Request path: /index
Request path: /favicon.ico
Request path: /cart
```

Screenshot of an actual run (visiting `/index` and `/cart` in turn; the `/favicon.ico` in between is the browser's automatic request, which falls into the 404 branch):

![[http-routing-terminal-paths.png]]

> The examples so far only handle GET requests — browsers send GET when visiting pages; POST is for submitting data to the server (e.g. forms). See 1.4.2 for the full list of methods and status codes.

## 4.5 Serving HTML Files from Disk

Real websites keep pages in files on disk, not inside code. Swap 4.4's routing branches from inline strings to "read a file by path", and you get the embryonic form of static file serving:

Complete runnable example: [static file server](../examples/en/http_server_static.py) (page files live in the [html/](../examples/en/html/) directory)

```python
# http_server_static.py
import os
import socket

# Absolute path of the html directory (based on this file's location, independent of the launch directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, 'html')

# 1. Create a TCP socket, bind the address, and start listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)
print("Serving on http://127.0.0.1:8000")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    path = request.split('\r\n')[0].split(' ')[1]
    print(f"Request path: {path}")

    # 2. Map the path to a file under html/; / defaults to index.html
    if path == '/':
        path = '/index.html'
    # lstrip('/') removes the leading slash so it is not treated as an absolute path
    file_path = os.path.join(HTML_DIR, path.lstrip('/'))

    # 3. Serve the file if it exists, otherwise the 404 page
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as f:
            body = f.read()
        status = '200 OK'
    else:
        with open(os.path.join(HTML_DIR, '404.html'), encoding='utf-8') as f:
            body = f.read()
        status = '404 Not Found'

    # 4. Reply in HTTP response format
    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
```

The two companion page files:

```html
<!-- html/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Home</title>
</head>
<body>
    <h1>Home</h1>
    <p>This page is served from the html/index.html file on disk.</p>
</body>
</html>
```

```html
<!-- html/404.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>404</title>
</head>
<body>
    <h1>404 Not Found</h1>
    <p>This page is served from the html/404.html file on disk.</p>
</body>
</html>
```

Run it and visit `http://127.0.0.1:8000/` to see the contents of `index.html`; any unknown path returns the `404.html` page with a 404 status code.

Two directions for going further:

- **`Content-Type` must follow the file type**: `.html` is `text/html`, `.css` is `text/css`, `.png` is `image/png` — the browser relies on it to decide how to render. A web framework's static directory (like Django's `static/`) is essentially a polished version of this exact logic.
- **Path safety**: a real server must guard against path traversal (e.g. `GET /../../etc/passwd`); this example skips it for teaching purposes.

## 4.6 Limitations of a Hand-Rolled Web Server

Working is not the same as production-ready. The server above has several obvious shortcomings:

- **One `recv(1024)` may not read the entire request** — this is exactly the sticky-packet/fragmentation problem from Chapter 3; a real implementation must read the body precisely according to `Content-Length`.
- **Only one connection at a time**: a slow client blocks every subsequent request (see 3.2 and 3.3 for concurrency options).
- **Routing, static files, and body parsing are all hand-written**: the code spirals out of control as features grow.
- **Each connection is closed after one request**: HTTP/1.0 style; HTTP/1.1 defaults to keep-alive, and a real implementation must declare the `Connection` behavior in its response headers.
- **Only GET is handled**: POST requests carry a body, which requires parsing `Content-Length` from the headers and then reading exactly that many bytes — another application of Chapter 3's "read the header, then read exactly that much" pattern.

In real development, web frameworks solve these problems: Django/Flask in Python, Express in Node, and so on. They are essentially HTTP parsing and routing layers built on top of sockets. The [Django tutorial](../../../web-development/django/) in this repository picks up from here.

> **Summary**: HTTP is a text protocol built on top of TCP. A socket server can talk to any browser as long as it replies in the "status line + headers + empty line + body" format. Hand-rolling a web server is the best exercise for understanding what web frameworks do under the hood.

[← Previous: Sticky Packets and Concurrency](03-sticky-packets-and-concurrency.md) | [Next: Project — A Simple Network Drive →](05-project-simple-network-drive.md)
