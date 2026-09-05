[← Previous: Responses](05-responses.md) | [Next: Request Hooks →](07-request-hooks.md)

# 6 Streaming Responses, Cookies and Sessions

This chapter covers three topics: streaming responses with generators (chunked transfer of large files, SSE event streams, etc.), and Flask's two mechanisms for recording user state — the client-side Cookie and the server-side Session (including using Redis as the Session backend).

## 6.1 Streaming Responses

A normal response returns all of its content to the client in one go; a streaming response splits the data into chunks and sends them one by one. It is suitable for large file downloads, real-time data push, and similar scenarios.

### 6.1.1 Units of Data Size

Before chunking files, let's clarify the common units:

- Bit: the smallest unit of data, representing 0 or 1;
- Byte (B): 1 Byte = 8 bit; a character usually takes 1 Byte, a Chinese character takes 2 Bytes;
- Kilobyte (KB): 1 KB = 1024 Byte (in binary computer systems), or 1 KB = 1000 Byte (in decimal labeling on storage devices);
- Megabyte (MB): 1 MB = 1024 KB.

### 6.1.2 Generator Recap

In Python, a generator is a special kind of iterator that produces a sequence of values instead of returning all values at once. There are two ways to create a generator:

- Generator expression: a list comprehension wrapped in parentheses, e.g. `(x for x in range(10))`;
- Generator function: a function containing a `yield` statement. Calling it returns a generator object instead of executing immediately; each `next()` call or `for` loop iteration runs the function up to the next `yield` statement.

Flask's streaming response works by passing a generator to the `Response` object.

### 6.1.3 Chunked Streaming of Large Files

```python
from flask import Flask, Response, stream_with_context
import time
import json
import os

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():
    # Large file -- chunking --> streaming response
    def generate():
        # Read file data ---> binary data, limiting the size of each read
        with open(os.path.join(os.getcwd(), 'fileUP',
                               '1d7346d9-956c-4145-a6a5-ca83ab6e51c8.jpg'), 'rb') as f:
            while True:
                # Read data in chunks  1024 B = 1 KB
                chunk = f.read(1024)
                if not chunk:
                    break
                yield chunk

    # Build the response object
    # stream_with_context: keeps the with context available during streaming
    #   ---> from flask import stream_with_context
    response = Response(stream_with_context(generate()),
                        mimetype="application/octet-stream")  # binary stream

    response.headers['Content-Disposition'] = 'inline;filename="index.jpg"'
    # response.headers['Content-Disposition'] = 'inline;filename="index.mp4"'
    # inline: the content is displayed directly in the browser (for supported formats such as PDF and images).
    # attachment: prompts the user to download the file, with filename specifying the default file name.

    return response


if __name__ == '__main__':
    print(app.url_map)  # view route information
    app.run(debug=True)
```

Key points:

- The generator function `generate()` reads 1 KB per `f.read(1024)` call and `yield`s each chunk until the file is exhausted, avoiding loading a large file into memory all at once;
- `stream_with_context(generate())` keeps the request context available during streaming;
- The `Content-Disposition` header controls how the browser handles the content: `inline` displays it directly, `attachment` triggers a download.

### 6.1.4 Passing a File Object Directly to Response

`Response` can also take a file object opened in binary mode directly; Flask iterates over it automatically:

```python
from flask import Flask, Response
import os

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():

    response = Response(open('./fileUP/1d7346d9-956c-4145-a6a5-ca83ab6e51c8.jpg', 'rb'),
                        mimetype="image/jpeg")

    # response.headers['Content-Disposition'] = 'inline;filename="index.jpg"'
    response.headers['Content-Disposition'] = 'attachment;filename="index.jpg"'
    # inline: the content is displayed directly in the browser (for supported formats such as PDF and images).
    # attachment: prompts the user to download the file, with filename specifying the default file name.

    return response


if __name__ == '__main__':
    print(app.url_map)  # view route information
    app.run(debug=True)
```

### 6.1.5 Other Common Streaming Response Forms

Text stream (progressively outputting loading messages):

```python
def generator():
    for i in range(10):
        yield f'loading {i}'
        time.sleep(1)

res = Response(generator(), mimetype='text/html')
print("is_streamed", res.is_streamed)  # is_streamed ---> True means a streaming response
return res
```

JSON stream (pushing JSON data item by item):

```python
def generator_json():
    for i in range(10):
        data = {
            'id': i,
            'message': f'level {i}',
            'time': time.time()
        }
        yield json.dumps(data)
        time.sleep(1.5)

return Response(generator_json(), mimetype='application/json')
```

SSE event stream (Server-Sent Events: the server keeps pushing events to the browser):

```python
# sse event stream --> sse format --> browser events
def event_s():
    for i in range(10):
        yield f'data:event {i}'
        time.sleep(1)

return Response(event_s(), mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',    # disable caching
                    'Connection': 'keep-alive',     # keep the connection alive
                    # 'X-Accel-Buffering': 'no'     # disable nginx buffering
                })
```

## 6.2 Cookies

### 6.2.1 What a Cookie Is and Its Characteristics

A Cookie is a small text file stored on the user's device, used to identify the user and track the session. It can record information such as the user's ID and pages visited, so that the site can provide a personalized experience on subsequent visits.

Cookies are stored as key-value pairs. Their characteristics:

- A Cookie is created by the server and sent to the client over HTTP (the `Set-Cookie` response header); the browser saves it and automatically carries it in every subsequent request;
- Storage limit: usually no more than 4KB;
- Two types: session cookies (expire when the browser is closed) and persistent cookies (with a set expiration period);
- Stored on the client, easy to read and manipulate via JavaScript;
- Low security: the data can be accessed by the user or other websites, so there is exposure risk, and cookies can be exploited by web attacks such as CSRF (Cross-Site Request Forgery) — an attacker crafts a malicious request (link) to impersonate the user. **Never store sensitive data in cookies**;
- Cookies have domain security restrictions: the browser only sends a cookie to the domain it belongs to;
- The lifecycle can be controlled with an expiration time, allowing long-term or short-term storage.

### 6.2.2 Setting, Reading and Deleting Cookies

```python
from flask import Flask, make_response, request

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():
    response = make_response('set cookie')

    # 1. Set a cookie ---> on the response object
    #    If the cookie key already exists, this becomes a modification
    #    set_cookie(key, value)
    response.set_cookie('username', 'admin')
    #    max_age ---> expiration time  unit: seconds
    # response.set_cookie('username', 'abai', max_age=60*60)

    # 2. Read a cookie ---> on the request object ---> cookies
    print(request.cookies.get('username'))

    # 3. Delete a cookie ---> on the response object ---> delete_cookie
    # response.delete_cookie('username')

    return response


if __name__ == '__main__':
    print(app.url_map)  # view route information
    app.run(debug=True)
```

Key points: setting and deleting cookies both operate on the **response object** (`set_cookie` / `delete_cookie`); reading a cookie operates on the **request object** (`request.cookies.get('key')`).

### 6.2.3 Cookie Expiration: max_age vs expires

`max_age` — **relative expiration time**, recommended because it is precise to the second:

- The unit is seconds; after receiving the cookie, the browser counts down from the current local time, and the cookie expires when the countdown ends;
- Corresponding response header: `Max-Age=3600`;
- Compatibility: an HTML5 standard, supported by all modern browsers; old IE browsers do not recognize `Max-Age`.

`expires` — **absolute expiration time**:

- Must be given a `datetime` object in UTC standard time; the cookie expires when the browser's local time reaches that moment;
- Corresponding response header: `Expires=Wed, 24 Jun 2026 22:14:00 GMT`;
- Compatibility: the only expiration field recognized by old browsers (IE6/7/8), fully compatible.

```python
import os
from flask import Flask, make_response
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():
    response = make_response('cookie expiration')

    # max_age ---- seconds (recommended, precise to the second)
    # response.set_cookie(key='username', value='admin', max_age=60*60)

    # expires ---> datetime object (UTC standard time)
    expires = datetime.utcnow() + timedelta(hours=1)
    response.set_cookie(key='username', value='admin', expires=expires)

    return response


if __name__ == '__main__':
    print('routes---:', app.url_map)
    app.run(debug=True)
```

### 6.2.4 Other set_cookie Parameters

```python
response.set_cookie(key='username', value='admin',
                    max_age=60*60,
                    domain='.baidu.com',
                    # path='/index',   # restrict to route paths with this prefix; default '/' ---> root path
                    # httponly=True,   # forbid JavaScript access
                    # secure=True,     # HTTPS only
                    )
```

- `domain`: restricts the domain the cookie belongs to. `domain='.baidu.com'` means `baidu.com` plus all matching subdomains (e.g. `www.baidu.com`, `baike.baidu.com`);
- `path`: the cookie is only sent with requests whose path matches this prefix; default `'/'` (root path, sent site-wide);
- `httponly=True`: forbids JavaScript from accessing the cookie, mitigating XSS theft;
- `secure=True`: the cookie is only transmitted over HTTPS.

## 6.3 Sessions

### 6.3.1 What a Session Is

Cookies are stored on the client; Sessions are stored on the server.

In web applications, a Session is known as "session control" — a special object created by the server to preserve user state. In short, a Session is an object for storing information on the server, suitable for sensitive data (personal private data). The main purpose of a Session is to record the user's state.

### 6.3.2 How Sessions Work

1. Creating a Session: when a user visits the server for the first time, the server creates a unique Session object for that user and generates a unique Session ID;
2. Storing the Session ID: the server stores the Session ID in the user's browser, usually via a Cookie;
3. Accessing the Session: in subsequent requests, the browser carries the Session ID; the server uses it to find the corresponding Session object, thereby reading or storing the user's state information.

### 6.3.3 The SECRET_KEY

The Session may still be visible in the browser (the Session ID in the cookie), and the Session may hold sensitive information, so Flask requires an encryption key (salt) `SECRET_KEY` to sign the Session data:

```python
import os

# 1. Manually define a fixed secret string (no Chinese characters or quotes)
app.config['SECRET_KEY'] = 'ADSFAWERFGSDCFA34583405()*&^%'

# 2. Randomly generate a secret key (suitable for projects that stay running for a long time)
# app.config['SECRET_KEY'] = os.urandom(24)
```

### 6.3.4 Setting, Reading, Deleting Sessions and Expiration

```python
import os
from datetime import timedelta
from flask import Flask, make_response, request, session

app = Flask(__name__, template_folder='templates')

# 1. Secret key --- SECRET_KEY
app.config['SECRET_KEY'] = 'ADSFAWERFGSDCFA34583405()*&^%'
# app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/index')
def index():
    # 2. Set a session ---> the session object ---> from flask import session
    session['username'] = 'abai'

    # 3. Read a session ---> get
    # print(session.get('username'))
    # print(session['username'])

    # 4. Delete a session -- pop deletes a specific key    clear empties everything
    # session.pop('username', None)
    # session.clear()

    # 5. Session expiration
    # Permanent session
    session.permanent = True
    # from datetime import timedelta
    # days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
    # Configure the session expiration on the Flask app instance; this sets the global session lifetime
    app.permanent_session_lifetime = timedelta(minutes=30)

    return "session"


if __name__ == '__main__':
    print(app.url_map)  # view route information
    app.run(debug=True)
```

Key points:

- `session` is imported from Flask and used like a dictionary: `session['key'] = value` to set, `session.get('key')` or `session['key']` to read;
- Delete with `session.pop('key', None)` (removes a specific key, no error if missing) or `session.clear()` (empties everything);
- `session.permanent = True` enables a permanent session, whose lifetime is controlled globally by `app.permanent_session_lifetime` (a `timedelta` object); without it, the Session expires when the browser is closed.

## 6.4 Storing Sessions in Redis

By default Flask stores Session data encrypted in the client-side cookie; with the `Flask-Session` extension, Session data can be stored in Redis on the server, and the browser only keeps the Session ID.

### 6.4.1 Installing Dependencies

```bash
pip install Flask-Session redis -i https://mirrors.aliyun.com/pypi/simple/
```

### 6.4.2 Configuration Options

- `SECRET_KEY`: the key used to sign the Session ID (must be set);
- `SESSION_TYPE`: specifies which backend to use; set it to `'redis'` here;
- `SESSION_PERMANENT`: whether to use permanent sessions (default `True`);
- `PERMANENT_SESSION_LIFETIME`: session lifetime (a `timedelta` object, default 31 days);
- `SESSION_USE_SIGNER`: whether to sign the Session ID in the cookie (recommended `True`);
- `SESSION_KEY_PREFIX`: the key prefix in Redis (default `'session:'`);
- `SESSION_REDIS`: the Redis connection instance (a connection object or a connection URL).

### 6.4.3 Configuration Example

```python
from flask import Flask, session
import redis
from flask_session import Session

app = Flask(__name__, template_folder='templates')

# 1. Configuration
app.config['SECRET_KEY'] = 'ADSFAWERFGSDCFA34583405()*&^%'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
app.config['SESSION_USE_SIGNER'] = True

# 2. Initialize the session
Session(app)


@app.route('/index', methods=['GET', 'POST'])
def index():
    session['name'] = 'chux'  # usage is exactly the same as the default session
    return 'session'


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```

After initializing `Session(app)`, reading and writing `session` in views works exactly the same, but the data is actually stored in Redis; the browser cookie only holds a signed Session ID (e.g. `G6eLi1ljiu7mMb0PBzrngZjNFnEzcNL-zxhAAl31fz4`).

[← Previous: Responses](05-responses.md) | [Next: Request Hooks →](07-request-hooks.md)
