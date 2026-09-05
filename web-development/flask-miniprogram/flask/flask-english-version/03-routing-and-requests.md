[← Previous: App Initialization Parameters and Routing](02-app-init-params-and-routing.md) | [Next: Requests and Responses →](04-requests-and-responses.md)

# 3 Routing and Requests

This chapter covers the core routing and request features of Flask: reverse URL resolution with `url_for`, dynamic routes and converters, custom regex converters, and the `request` object used to access incoming request data.

## 3.1 Reverse Resolution with url_for

During project development, changing a route is painful: every place that hardcodes the route must be updated as well. Reverse resolution solves this problem by generating the real route path from the **endpoint name**. By default, the endpoint is the same as the view function name.

`url_for` must be imported from flask: `from flask import url_for`.

```python
from flask import Flask, request, url_for

app = Flask(__name__)


@app.route('/index12334', methods=['GET', "POST"])
def index():
    print(url_for('index'))    # reverse-resolve the real path from the endpoint: /index12334
    return 'index'


if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

Additional notes:

- `app.add_url_rule` is another way to register a route, allowing the endpoint to be set explicitly:

```python
app.add_url_rule('/index', endpoint='index', view_func=index)
# resulting rule: <Rule '/index' (HEAD, GET, OPTIONS) -> index>

app.add_url_rule('/index', endpoint='index123', view_func=index)
# resulting rule: <Rule '/index' (OPTIONS, GET, HEAD) -> index123>
```

- A route rule has the full form `<Rule 'path' (methods) -> endpoint>`; `url_for` looks up the path by endpoint.

## 3.2 Dynamic Routes

Dynamic routes extract data from the URL path and pass it into the view. For example, visiting `http://127.0.0.1:5000/index/2025` extracts `2025` from the path and passes it to the view function. There are several ways to do this.

### 3.2.1 Direct Extraction (str by Default)

Name the path segment to extract with `<variable>` in the route; the view function must accept a parameter with the same name:

```python
from flask import Flask

app = Flask(__name__)


# http://127.0.0.1:5000/index/2025 ---> extract 2025 and pass it to the view
# route rule: <Rule '/index/<year>' (GET, HEAD, OPTIONS, POST) -> index>
@app.route('/index/<year>', methods=['GET', "POST"])
def index(year):  # note: accept the parameter; it is of type str by default
    print(year)
    return 'index'


if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

### 3.2.2 Built-in Converters

Use the `<converter:variable>` form to constrain the parameter type. Common built-in converters:

| Converter | Description |
| --------- | ----------- |
| `int` | Matches integers |
| `float` | Matches floating-point numbers |
| `path` | Matches paths containing `/` (the default converter does not match `/`) |

```python
# match an integer: http://127.0.0.1:5000/index/2025
@app.route('/index/<int:year>', methods=['GET', "POST"])
def index(year):  # note: accept the parameter
    print(year)
    return 'index'


# match a float: http://127.0.0.1:5000/index/2025.9
@app.route('/index/<float:year>', methods=['GET', "POST"])
def index(year):  # note: accept the parameter
    print(year)
    return 'index'


# match a path containing /: http://127.0.0.1:5000/index/2025.9/
@app.route('/index/<path:year>', methods=['GET', "POST"])
def index(year):  # note: accept the parameter
    print(year)  # 2025.9/
    return 'index'
```

## 3.3 Custom Regex Converters

When the built-in converters are not enough, you can define a custom converter based on a regular expression.

### 3.3.1 Definition and Registration

A custom converter must inherit from `werkzeug.routing.BaseConverter` and override its `__init__` method; it is then registered through `app.url_map.converters` (`url_map` holds all route converters and is of dict type):

```python
from flask import Flask, url_for
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):  # *args: variable-length arguments ---》 receive the regex data
        # inherit the original initialization logic
        super(RegexConverter, self).__init__(url_map)
        # update the regex data
        self.regex = args[0]

    # operations after the converter extracts data
    # def to_python(self, value):
    #     print(f"converter received data: {value}, type: {type(value)}")
    #     return value

    # when reverse-resolving a route with a converter
    # def to_url(self, value):
    #     print(f"reverse resolution ---》 converter received data: {value}, type: {type(value)}")
    #     return value


# register the converter: converter name    converter class
app.url_map.converters['re'] = RegexConverter
```

Usage (watch out for string escaping — prefix the route string with `r`):

```python
# http://127.0.0.1:5000/index/2025 ---> extract 2025 --》 pass it to the view
@app.route(r'/index/<re("\d+"):year>', methods=['GET', "POST"])
def index(year):  # note: accept the parameter
    print(year)
    return 'index'
```

### 3.3.2 Reverse Resolution with url_for

Routes with converters can also be reverse-resolved; pass the parameter by variable name in `url_for`:

```python
@app.route('/demo')
def demo():
    print(url_for('index', year="2018"))  # reverse-resolves to /index/2018
    return 'demo'


if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

## 3.4 The request Object

Flask handles request data differently from Django: a Django view's first parameter must be the HttpRequest object, whereas in Flask you import the `request` object from flask, which already encapsulates all request parameters.

Data flow: the client (browser) sends a request for data (carrying standard data) → the flask server parses the data → the `request` object.

### 3.4.1 Overview of Common Attributes

| Attribute | Core Function and Description | Data Type |
| --------- | ------------------------------------------------------------ | ------------------- |
| `form`    | Stores the **form key-value data** submitted in POST/PUT requests (e.g. username and password on a login page). Note: uploaded files are **not stored here** — they are stored in the `files` attribute. | `MultiDict` |
| `args`    | Stores the **query string parameters after the question mark** in the URL (i.e. GET request parameters, such as `?id=1&name=test`). | `MultiDict` |
| `values`  | Merges everything from `form` and `args`; no need to distinguish request methods — access all parameters uniformly. | `CombinedMultiDict` |
| `cookies` | Stores **all Cookie data** carried by the client in the current request; can directly read login state, preferences, etc. | `dict` |
| `headers` | Stores **all request header information** (e.g. User-Agent, Content-Type, Token); a dict-like readable object. | `dict` |
| `method`  | Identifies the **HTTP method** of the current request; common values are `GET`, `POST`, `PUT`, `DELETE`, etc. Useful for handling different request logic on the same route. | `string` |
| `files`   | Stores **all uploaded file data** from POST/PUT requests. Each file is a `FileStorage` object with a built-in `save()` method that saves the uploaded file directly to the server file system. | `MultiDict` |

Path-related attributes: `path`, `script_root`, `url`, `base_url`, `url_root`.

Additionally, `request.json` is used to access JSON request body data (non-form data).

Query string example: in `https://cn.bing.com/search?q=csdn...`, everything after `?` is the query string data, accessed via `request.args`.

### 3.4.2 Examples of Accessing Request Data

```python
from flask import Flask, request

app = Flask(__name__)


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # form data
    # print(request.form)  # ImmutableMultiDict([('name', 'abai'), ('happy', '1')])

    # non-form data --- json
    # print(request.json)  # {'name': 'abai', 'age': 18}

    # get all parameters (args + POST form, excluding non-form data)
    print(request.values)
    # CombinedMultiDict([ImmutableMultiDict([('a', '1'), ('a', 'shuai')]),
    # ImmutableMultiDict([('name', 'abai'), ('happy', '1')])])

    # get returns only the first value; getlist returns all values of the key
    print(request.values.get('a'))
    print(request.values.getlist('a'))  # ['1', 'shuai', '1990']

    # query string
    # print(request.args)  # ImmutableMultiDict([('a', '1')])
    # print(request.args)  # ImmutableMultiDict([('a', '1'), ('a', 'shuai')])
    # print(request.args.get('a'))  # 1
    # print(request.args.getlist('a'))  # ['1', 'shuai']

    # path-related attributes
    # print(request)  # <Request 'http://127.0.0.1:5000/demo?a=1' [GET]>
    # print(request.path)     # /demo
    # print(request.url)      # http://127.0.0.1:5000/demo?a=1
    # print(request.base_url) # http://127.0.0.1:5000/demo
    # print(request.url_root) # http://127.0.0.1:5000/
    return 'demo'


if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

Key points:

- `MultiDict` / `ImmutableMultiDict` allow multiple values per key: `.get('key')` returns only the first value, while `.getlist('key')` returns a list of all values for that key.
- `request.values` merges the query string and form data (`args` + `form`), but does not include non-form data such as JSON.
- Accessing a route with a method it does not declare returns `405 Method Not Allowed`.

### 3.4.3 File Upload

Flask's data flow for handling client file uploads: file data is stored in memory or a temporary file system location → retrieved via the `request.files` attribute (ImmutableMultiDict) → get the `FileStorage` file object by key → call its `save()` method to save it to a specified path on the server file system.

```python
import os
from hashlib import md5

from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST'])
def demo():
    # request.files ImmutableMultiDict([('ttt', <FileStorage: '001.png' ('image/png')>)])
    # print("request--file", request.files)

    # get the file object by key
    # request--file <FileStorage: '001.png' ('image/png')>
    # print("request--file", request.files.get('ttt'))

    # save method: save directly to the given path
    # request.files.get('ttt').save("ces.png")

    # sanitizing the file name
    # secure_filename: pass in a file name, get back a safe file name
    # Chinese characters are removed entirely; spaces are replaced with underscores
    # print("secure_filename", secure_filename(request.files.get('ttt').filename))

    # real development scenario ----》 flexible absolute paths
    # os.getcwd(): get the absolute path of the current file's directory
    # print("os.getcwd()", os.getcwd())

    # build the absolute path of the upload directory ----》 path joining: os.path.join()
    fileCWD = os.path.join(os.getcwd(), "fileUP")

    # make sure the directory exists: check first (os.path.exists) ---》 create if missing
    if not os.path.exists(fileCWD):
        os.makedirs(fileCWD)  # create the directory

    # get the file object
    f = request.files.get('ttt')

    # using a user-supplied file name directly is dangerous and bug-prone
    # the right approach: generate a unique file name yourself (timestamp, random number, uuid, etc.)
    # md5-based safe file name: the same data always produces the same md5 hash
    # encode the string first with encode('utf-8'); hexdigest() returns the hash
    md5_filename = md5(f.filename.encode("utf-8")).hexdigest()
    # e.g.: c36625d731a8602531c9ad084b74b3bf

    # get the file extension
    o_filename = f.filename  # e.g. demo.py
    d_index = o_filename.rindex('.')  # right index
    file_su = o_filename[d_index:]

    # join the new file name and save
    new_filename = md5_filename + file_su
    save_path = os.path.join(fileCWD, new_filename)
    f.save(save_path)

    return 'demo'


if __name__ == '__main__':
    print(app.url_map)  # view routing information
    app.run(debug=True)
```

Key points:

- `secure_filename()` sanitizes file names: Chinese characters are removed entirely and spaces are replaced with underscores.
- Saving under a user-supplied file name is dangerous; the right approach is to generate a unique name yourself (timestamp, random number, uuid, or md5 + original extension as in this example).
- `os.getcwd()` gets the absolute path of the current directory, `os.path.join()` joins paths, and `os.path.exists()` + `os.makedirs()` ensure the save directory exists.

[← Previous: App Initialization Parameters and Routing](02-app-init-params-and-routing.md) | [Next: Requests and Responses →](04-requests-and-responses.md)
