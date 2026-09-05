[← Previous: Requests and Responses](04-requests-and-responses.md) | [Next: Streaming Responses, Cookies and Sessions →](06-streaming-responses-cookies-and-sessions.md)

# 5 Responses

This chapter covers the common ways of building responses in Flask: template responses (manual construction and `render_template`), exception responses (`abort` and `errorhandler`), redirect responses (`redirect` and `url_for`), and generator-based streaming responses.

## 5.1 Template Responses

There are two approaches to returning an HTML template:

- Approach 1: manual construction (`make_response` + `open` to read the file + `re.sub` to inject data)
- Approach 2: using Flask's built-in `render_template`

### 5.1.1 Manually Building a Template Response

First, prepare a template file `templates/demo.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Template test</title>
</head>
<body>
<h1>Hello ---- {{ name }}</h1>

</body>
</html>
```

The manual approach: build a response object with `make_response()`, read the template file content with `open`, replace the placeholders in the template with actual data using regular expressions, then assign the processed content to the response body and return it:

```python
from flask import Flask, render_template, make_response
import re

app = Flask(__name__, template_folder='templates')

"""
Template responses:
---- Approach 1: manual construction
---- Approach 2: render_template
"""

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    name = 'abai'
    # Approach 1: manual construction
    # --------- build the response object with make_response
    respose = make_response()
    # --------- custom response body: open the file (path, mode, encoding) and read it
    data = open('./templates/demo.html', 'r', encoding='utf-8').read()

    # Template data injection
    """
    import re

    re.sub ---> matches substrings in the target string with a regular expression
    and replaces them with the given content (string / function return value)

    sub(pattern, repl, string, count=0, flags=0):
        pattern: regex pattern used to match the substrings to replace
        repl:   replacement content --- string / function return value
        string:  the original string to process
        count: maximum number of replacements ---- default 0, replace all matches
        flags: regex flags
            ----  re.IGNORECASE: ignore case
            ----  re.DOTALL: match newlines
    """
    # the pattern argument must exactly match the placeholder in the template page
    data = re.sub('{{ name }}', name, data)

    respose.data = data
    return respose

if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

Key points: `re.sub(pattern, repl, string)` matches substrings in the template string with a regular expression and replaces them; the `pattern` must exactly match the placeholder as written in the template page (including whitespace).

### 5.1.2 Using render_template

`render_template` is Flask's built-in template rendering approach. You only need to pass the template name and the variables to inject — no manual file reading or regex replacement required:

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    name = 'abai'
    # return render_template('demo.html')
    # return render_template('demo.html', name=name)
    age_size = 18
    return render_template('demo.html', name=name, age=age_size)

if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

The template receives variables through placeholders such as `{{ name }}` and `{{ age }}`. Clearly, `render_template` is far more concise than manual construction and is the standard practice in real development.

## 5.2 Responses — Exceptions

### 5.2.1 The abort Function

The `abort` function abandons the request and returns an error code (response status code). Once `abort` is called, the view terminates immediately and the code after it never runs:

```python
from flask import Flask, abort

app = Flask(__name__, template_folder='templates')

"""
abort function: abandon the request and return an error code (response status code)
"""

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # terminate the view and return an HTTP status
    abort(404)
    # abort(404, 'Error message 404')
    return "hello"

if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

### 5.2.2 Custom Error Handling Views (errorhandler)

The `errorhandler` decorator takes an HTTP status code as its argument and defines a custom error handling view for that code. It applies not only to errors raised by the `abort` function, but also to the corresponding error codes produced by the Flask application itself (for example, a 404 triggered by accessing a route that does not exist):

```python
@app.errorhandler(404)
def not_found(error):  # the error information object
    return f'Address not found {error}'
```

Note: `errorhandler` cannot accept an invalid custom error code — doing so raises a `ValueError`:

```python
# ValueError: '4000000' is not a recognized HTTP error code.
# Use a subclass of HTTPException with that code instead.
# @app.errorhandler(4000000)
# def not_found(error):  # the error information object
#     return f'Address not found {error}'
```

## 5.3 Responses — Redirection

Use `redirect` for redirection, usually together with `url_for`: `url_for` reverse-resolves the real route URL from the view function name, and `redirect` then redirects to that URL — avoiding hardcoded URLs in the code:

```python
from flask import Flask, redirect, url_for

app = Flask(__name__, template_folder='templates')

"""
redirect: redirection
"""

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    print("logging in")
    # return redirect('/index')
    # reverse resolution ----》 real route ---》 redirect
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return "index --- login complete"

if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

## 5.4 Streaming Responses

A streaming response does not return all data at once, but sends it in batches, step by step. Typical use cases:

- Real-time data push
- Large file transfer
- Progress updates for long-running tasks

### 5.4.1 Generator Basics

Streaming responses rely on Python generators. A generator is a special kind of iterator that produces data on demand (lazy evaluation) instead of loading all results into memory at once. It relies on the `yield` keyword to "pause and resume" a function, making it ideal for handling large data sets or infinite sequences.

Unlike a normal function, a generator function does not execute immediately when called — it returns a generator object. Each call to `next()`, or each iteration in a `for` loop, resumes execution from where it last paused, until the next `yield` or the end:

```python
>>> ga = generate()
>>> ga
<generator object generate at 0x000001C7E07B0040>
>>> next(ga)
0
>>> next(ga)
1
...
>>> next(ga)
9
>>> next(ga)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration     ----> the generator is exhausted
```

### 5.4.2 Basic Streaming Response

Pass a generator to `Response`, and Flask will send the data piece by piece in a streaming fashion. You can verify it is a streaming response with `response.is_streamed`:

```python
from flask import Flask, redirect, url_for, Response
import time

app = Flask(__name__, template_folder='templates')

@app.route('/index')
def index():
    # generator  closure
    def generate():
        for i in range(10):
            yield f"data: {i} <br>"
            time.sleep(1)

    response = Response(generate(), mimetype='text/html')
    print(response.is_streamed)  # is_streamed True ---> streaming response
    return response

if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

When you visit `/index` in a browser, the data appears piece by piece, one line per second, instead of all at once after 10 seconds.

### 5.4.3 JSON Streaming Response

A generator can also produce JSON data piece by piece, with the `mimetype` set to `application/json`:

```python
import json

@app.route('/index')
def index():
    def generate_json():
        for i in range(10):
            data = {
                "id": i,
                "message": f"message {i}",
                "timestamp": time.time()
            }
            yield json.dumps(data)
            time.sleep(1)

    return Response(generate_json(), mimetype='application/json')
```

### 5.4.4 SSE Event Stream

SSE (Server-Sent Events) is the standard way for browsers to receive an event stream. The generator yields data in SSE format (each line starting with `data: `), and the response `mimetype` is set to `text/event-stream`:

```python
@app.route('/index')
def index():
    # sse event stream ----》 sse format ---》 browser events
    def event_stream():
        for i in range(10):
            yield f'data: event {i} \n'
            time.sleep(1)

    # text/event-stream ---> sse
    return Response(
        event_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',   # no-cache disables caching
            "Connection": "keep-alive",     # keep-alive keeps the connection open
            # "X-Accel-Buffering": "no",    # disable nginx buffering
        }
    )
```

### 5.4.5 Response Headers Related to Streaming

Common `Cache-Control` values:

- `max-age=`: sets the maximum time (in seconds) the cache is considered fresh. Example: `Cache-Control: max-age=3600` means the cache is valid for 1 hour.
- `no-cache`: requires the cache to validate the resource with the server before using it. Even if a cached copy exists, it must be revalidated. Example: `Cache-Control: no-cache`.
- `no-store`: completely disables caching — neither the client nor proxy servers may store any part of the request or response. Example: `Cache-Control: no-store`.
- `public`: allows any cache (including proxy servers) to store the response content. Example: `Cache-Control: public, max-age=86400`.
- `private`: only allows a single user's local cache to store the content; proxy servers must not cache it. Example: `Cache-Control: private, max-age=3600`.
- `must-revalidate`: once the cache expires, the resource must be revalidated with the server. Example: `Cache-Control: must-revalidate`.
- `immutable`: indicates the response content will not change over time, so the client does not need to revalidate it, even when the user refreshes the page. Example: `Cache-Control: immutable`.
- `stale-while-revalidate=`: allows the client to use a stale cache while asynchronously revalidating it in the background. Example: `Cache-Control: stale-while-revalidate=60`.
- `stale-if-error=`: allows the client to use a stale cache when the server encounters an error. Example: `Cache-Control: stale-if-error=120`.

Common `Connection` values:

- `Connection: keep-alive`: `keep-alive` keeps a persistent connection, allowing multiple requests to reuse the same TCP connection. Its advantages include reduced connection setup/teardown overhead, lower network latency, and better system performance. In HTTP/1.1, persistent connections are enabled by default and require no extra configuration on either side.
- `Connection: close`: `close` means a short-lived connection that is closed immediately after each request completes. In HTTP/1.0, this is the default behavior.

[← Previous: Requests and Responses](04-requests-and-responses.md) | [Next: Streaming Responses, Cookies and Sessions →](06-streaming-responses-cookies-and-sessions.md)
