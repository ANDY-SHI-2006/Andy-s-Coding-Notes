[← Previous: Streaming Responses, Cookies and Sessions](06-streaming-responses-cookies-and-sessions.md) | [Next: Contexts and Templates →](08-contexts-and-templates.md)

# 7 Request Hooks

## 7.1 Overview of Request Hooks

The complete lifecycle of a request looks like this:

```
client --- request --- Flask app --- response

inside the Flask app:  request ---> view ---> response
```

Request hooks are handler functions plugged into this "request → view → response" pipeline. They can run shared logic (such as permission checks, logging, or resource cleanup) before entering a view, after the view finishes, or when the request ends.

Flask provides three commonly used request hooks:

| Hook | When it fires |
| ---- | ------------- |
| `app.before_request` | Before entering the view |
| `app.after_request` | After the view has finished processing |
| `app.teardown_request` | When the request ends (also fires on view exceptions) |

## 7.2 Using the Three Request Hooks

- `before_request`: takes no arguments; runs before the view function.
- `after_request`: receives the response object returned by the view and **must return a response object** after processing.
- `teardown_request`: receives the exception object; it fires even when no exception was raised (in that case the exception object is `None`).

```python
from flask import Flask

app = Flask(__name__,
            template_folder='templates')


@app.before_request
def before_request():
    print('before_request runs')


@app.after_request
def after_request(response):  # receive the response object
    print('after_request runs')
    return response  # return the response object


@app.teardown_request
def teardown_request_(exception):  # receive the exception object
    print('teardown_request fired: ', exception)
    return exception  # return the data object


@app.route('/index')
def index():
    return 'exception'


if __name__ == '__main__':
    print('routes---:', app.url_map)

    app.run(debug=True)
```

### 7.2.1 What Happens When the View Raises an Exception

When a view function raises an exception (for example `a = 1/0`), `after_request` is not executed, but `teardown_request` still fires and receives the exception object:

```python
@app.route('/index')
def index():
    print('index')
    a = 1/0  # raises ZeroDivisionError
    return "request hooks"
```

After visiting `/index`, the console prints `teardown_request fired: ` along with the corresponding exception. You can take advantage of this to do centralized exception logging and resource cleanup in `teardown_request`.

## 7.3 Passing Data Between Hook Functions and View Functions

When you need to pass data between hook functions and view functions, use Flask's `g` object as a global variable. `g` is scoped to the application and is rebuilt (cleared first) for every incoming request, so you can write data in `before_request` and read it in the view function:

```python
from flask import Flask, g

app = Flask(__name__,
            template_folder='templates')


@app.before_request
def before_request():
    g.s = 'value passed via the g object'


@app.route('/index')
def index():
    print(g.s)         # value passed via the g object
    # print(g.get('s'))  # you can also read it with get
    return "request hooks"


if __name__ == '__main__':
    print('routes---:', app.url_map)

    app.run(debug=True)
```

> The `g` object is part of Flask's contexts. See Chapter 8 for a detailed introduction to the application context and the request context.

## 7.4 Supplement: Storing Sessions in Redis

By default, Flask stores session data in client-side cookies. With the `Flask-Session` extension, session data can be stored in a Redis server instead:

- Using Redis with Flask: `redis` (the Redis driver module)
- Building Redis-backed session storage: `Flask-Session`

Install the dependencies:

```bash
pip install Flask-Session redis -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 7.4.1 Common Configuration Options

- `SECRET_KEY`: the key used to sign the Session ID (must be set).
- `SESSION_TYPE`: which backend to use; set it to `'redis'` here.
- `SESSION_PERMANENT`: whether to use permanent sessions (default `True`).
- `PERMANENT_SESSION_LIFETIME`: session lifetime (a `timedelta` object, default 31 days).
- `SESSION_USE_SIGNER`: whether to sign the Session ID in the cookie (`True` recommended).
- `SESSION_KEY_PREFIX`: the key prefix in Redis (default `'session:'`).
- `SESSION_REDIS`: the Redis connection instance (a connection object or a connection URL).

### 7.4.2 Complete Example

```python
import os
from datetime import timedelta
from flask import Flask, make_response, request, session
import redis
from flask_session import Session

app = Flask(__name__,
            template_folder='templates')

# 1. encryption key --- SECRET_KEY
app.config['SECRET_KEY'] = 'f*&……*（）#￥%%&iehrjgjakjsdbveiwjfdgfi(*(&*^%$^&YR&*^YH&'
app.config["SESSION_TYPE"] = 'redis'
app.config["SESSION_REDIS"] = redis.from_url('redis://127.0.0.1:6379')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

# initialize Session
Session(app)


@app.route('/index')
def index():
    session['name'] = 'abai'
    return "session"


if __name__ == '__main__':
    print(app.url_map)  # inspect route information

    app.run(debug=True)
```

### 7.4.3 Verifying in Redis

After visiting `/index` to write the session, you can inspect the stored result with `redis-cli`:

```
C:\Users\abai>redis-cli

127.0.0.1:6379> keys *
1) "session:a4eM9SKd7Z4AwHw2w4MPuKcUrAEj4eKvRp_viqL3CzE"
2) "session:Yod0uke9efw2PI5Yo1rNMAaWIVaEWItM2_O_8T3Baco"
3) "session:U4YCVQLPQHnL5zHFSj0fCmkWSaQHq7z6-XI9FTL1j20"

127.0.0.1:6379> get "session:U4YCVQLPQHnL5zHFSj0fCmkWSaQHq7z6-XI9FTL1j20"
"\x81\xa4name\xa4abai"
```

As you can see, the session data is stored in Redis under keys with the `session:` prefix, and the value is the serialized `{'name': 'abai'}`.

## 7.5 Supplement: Cookie Expiration with expires

There are two ways to set a cookie's expiration: `max_age` and `expires`. **`max_age` is recommended** because it is precise to the second.

```python
import os
from datetime import timedelta, datetime
from flask import Flask, make_response, request, session

app = Flask(__name__,
            template_folder='templates')


@app.route('/index')
def index():
    # max_age ---- seconds
    response = make_response('cookie expiration')

    # expires ---> a datetime object
    # expires = datetime.now() + timedelta(hours=1)
    expires = datetime.utcnow() + timedelta(hours=1)
    response.set_cookie('username', 'admin', expires=expires)

    return response


if __name__ == '__main__':
    print(app.url_map)  # inspect route information

    app.run(debug=True)
```

### 7.5.1 The Timezone Pitfall of expires

`expires` accepts a `datetime` object. The related time arithmetic:

```
>>> from datetime import timedelta, datetime

>>> datetime.now()
datetime.datetime(2026, 3, 7, 20, 31, 39, 895878)

>>> timedelta(hours=1)
datetime.timedelta(seconds=3600)

>>> datetime.now() + timedelta(hours=1)
datetime.datetime(2026, 3, 7, 21, 32, 23, 62567)
```

If you set the expiration with `datetime.now()` (local time), the time shown in the browser's site information will differ from what you expect — the browser treats your time as UTC standard time and then converts it to the local timezone. For example:

- Created: March 7, 2026, 20:30:01; expected to expire 1 hour later, i.e. 21:30:01;
- Actually shown as expiring: March 8, 2026, 05:30:01 — 8 hours off the correct result.

The reason is that China's timezone is UTC+8, which is 8 hours ahead of international standard time. Therefore, when using `expires`, compute the expiration with `datetime.utcnow()` to avoid the timezone offset.

## 7.6 Supplement: set_cookie Parameters

Besides `key`, `value`, and `max_age`/`expires`, `set_cookie` has several commonly used restriction parameters:

```python
import os
from datetime import timedelta, datetime
from flask import Flask, make_response, request, session

app = Flask(__name__,
            template_folder='templates')


@app.route('/index')
def index():
    # max_age ---- seconds
    response = make_response('cookie expiration')
    response.set_cookie('username', 'admin',
                        max_age=60*60,
                        domain='127.0.0.1'
                        # domain='.baidu.com'   # only valid for the configured host name
                        # domain='baidu.com'
                        # path='/index'  # prefix restriction on the route path
                        # path='/'       # prefix restriction on the route path -- default / ---> root path
                        # httponly=True  # forbid JavaScript access
                        # secure=True    # HTTPS only
                        )
    return response


if __name__ == '__main__':
    print(app.url_map)  # inspect route information

    app.run(debug=True)
```

Parameter reference:

| Parameter | Effect |
| --------- | ------ |
| `max_age` | Expiration time in seconds (recommended) |
| `domain` | Restricts the domain for which the cookie is valid |
| `path` | Prefix restriction on the route path; default `/` (root path) |
| `httponly` | When `True`, JavaScript cannot access the cookie |
| `secure` | When `True`, the cookie is only sent over HTTPS requests |

About `domain`: setting it to `baidu.com` (or `.baidu.com`) makes the top-level domain match all subdomains:

```
baidu.com     matches all subdomains
---> www.baidu.com
---> baike.baidu.com
```

[← Previous: Streaming Responses, Cookies and Sessions](06-streaming-responses-cookies-and-sessions.md) | [Next: Contexts and Templates →](08-contexts-and-templates.md)
