[← Previous: Routing and Requests](03-routing-and-requests.md) | [Next: Responses →](05-responses.md)

# 4 Requests and Responses

This chapter covers two advanced request/response topics in Flask: how to receive and save files uploaded by the client in a request, and how to flexibly build response objects (basic responses and JSON responses).

## 4.1 Request — File Upload

When Flask handles file data sent by the client, the file is first stored in memory or at a temporary location in the file system. It is accessed through the `files` attribute of the `request` object:

- `request.files` is a `MultiDict`; you retrieve the file data object by the form field name (the key);
- The retrieved file object is of type `FileStorage`;
- Calling the `FileStorage` object's `save()` method with a destination path saves the file to the server's file system.

### 4.1.1 Getting the Uploaded File

```python
from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from hashlib import md5

app = Flask(__name__)

"""
When Flask handles incoming file data from the client, it stores it in memory
or at a temporary location in the file system.
------ request object ---》 files attribute holds the file data: MultiDict
------ get the file data object by key: FileStorage
------ FileStorage object ---》 save method: save to the server's file system ---》 destination path
"""

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # form data
    # ImmutableMultiDict([('my_files', <FileStorage: '1d7346d9-956c-4145-a6a5-ca83ab6e51c8.jpg' ('image/jpeg')>)])
    print(request.files)
    # <FileStorage: '1d7346d9-956c-4145-a6a5-ca83ab6e51c8.jpg' ('image/jpeg')>
    print(request.files.get('my_files'))
    # 1d7346d9-956c-4145-a6a5-ca83ab6e51c8.jpg
    print(request.files.get('my_files').filename)

    # mime type
    # print(request.content_type)  # multipart/form-data; boundary=------------------------823013153256183608392438

    return 'demo'

if __name__ == '__main__':
    print(app.url_map)  # view routing info
    app.run(debug=True)
```

Key points:

- `request.files` prints as an `ImmutableMultiDict`; the key is the name of the file field in the form (`my_files` here), and the value is a `FileStorage` object;
- `request.files.get('my_files')` retrieves the file object, whose `.filename` attribute is the original filename from the client;
- The `Content-Type` of a file upload request is `multipart/form-data` with a boundary delimiter.

### 4.1.2 Making the Filename Safe

Saving a file directly under the name supplied by the client is a security risk, so the filename must be processed first.

**Option 1: `secure_filename`**

`secure_filename` takes a filename and returns a safe version of it:

```python
from werkzeug.utils import secure_filename

print(secure_filename(request.files.get('my_files').filename))
```

Examples of the effect:

- Filenames containing Chinese characters don't work: `雪人.jpg` → `jpg` (the Chinese part is dropped)
- `logo配色图-2.png` → `logo-2.png`
- `WIN 20231022_23_25_11_Pro.jpg` → `WIN_20231022_23_25_11_Pro.jpg` (spaces are replaced with underscores)

**Option 2: md5-based filename sanitization**

md5 is used for data hashing — the same data always produces the same MD5 hash. The string to hash must first be encoded with `encode('utf-8')`, then `hexdigest()` returns the hash result:

```python
from hashlib import md5

# hash the filename with md5
md5_filename = md5(request.files.get('my_files').filename.encode('utf-8')).hexdigest()
# WIN 20231022_23_25_11_Pro.jpg ----> bfc4e00e42b10f8c9f371a505f7241f8
# print(md5_filename)

# get the file extension  WIN 20231022_23_25_11_Pro.jpg
old_filename = request.files.get('my_files').filename
dot_index = old_filename.rindex('.')  # rindex ---> right index
# print(dot_index)  # 25
file_suffix = old_filename[dot_index:]  # .jpg
# print(file_suffix)
new_filename = md5_filename + file_suffix
# print(new_filename)  # bfc4e00e42b10f8c9f371a505f7241f8.jpg
```

The idea: hash the original filename with md5 to get a unique, safe string, then use `rindex('.')` to extract the original file extension and append it to the new filename.

### 4.1.3 Building the Save Path and Saving the File

In real development you should use a flexible absolute path:

```python
# os.getcwd(): get the absolute path of the current working directory
# print(os.getcwd())  # E:\pythonfile\flask0228

# build the absolute path of the upload directory ---- path joining with os.path.join()
fileCWD = os.path.join(os.getcwd(), 'fileUP')

# make sure this directory exists: check first (os.path.exists) ---》 if not: create it
if not os.path.exists(fileCWD):  # if the directory specified by fileCWD does not exist
    os.makedirs(fileCWD)  # create directory: os.mkdir;  os.makedirs ---》 creates nested directories

f = request.files.get('my_files')
# full save path of the file
sava_file = os.path.join(fileCWD, f.filename)
f.save(sava_file)
```

A simpler way to save (directly into the current working directory):

```python
# save ---- get the filename from the file object's filename attribute
f = request.files.get('my_files')
f.save(f.filename)

# or specify a filename explicitly
request.files.get('my_files').save('ceshi.jpg')
```

## 4.2 Response — Basic Response

References:

- MIME types: <https://www.runoob.com/http/mime-types.html>
- Status codes: <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Status>

A full request-response cycle is: `client ---request---》 server ---response---》 client`. What the server returns to the client is a response object, which consists of three parts: **response data, response status code, and response headers**.

There are three ways for a view function to build a response:

1. `return` a string — the response object is built from the string plus default parameters;
2. `return` a tuple — it must contain (response data, status, headers); the headers are a dictionary and must not contain Chinese characters or special symbols;
3. Use `make_response` to build a proper response object: `from flask import make_response`.

```python
from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # case 1: return a string directly
    # return 'demo'

    # case 2: return a tuple (response data, status code, headers dict)
    # return ('demos', 200, {'Content-Type': 'text/plain'})
    # return ('demos', 200, {'Content-Type': 'text/plain', "demo": 'abai'})

    # header values must not contain Chinese characters, otherwise an encoding error is raised:
    # UnicodeEncodeError: 'latin-1' codec can't encode character '\u963f' in position 10: ordinal not in range(256)
    # return ('demos', 200, {'Content-Type': 'text/plain', "demo": 'abai阿'})

    # case 3: build the response object with make_response
    # return make_response('hello world')
    respose = make_response()
    # response data
    respose.data = 'flask 框架'
    # status code
    respose.status_code = 200
    # response headers
    respose.content_type = 'text/plain'
    # respose.content_type = 'text/plain; charset=UTF-8'
    respose.headers['demo'] = 'abai'

    return respose

if __name__ == '__main__':
    print(app.url_map)  # view routing info
    app.run(debug=True)
```

Key points:

- With the tuple form, if a header value contains Chinese characters (e.g. `'abai阿'`), a `UnicodeEncodeError: 'latin-1' codec can't encode character ...` is raised — whenever Web programming is involved, encoding issues come along;
- `make_response()` can create an empty response object first, then you set `data` (response data), `status_code` (status code), `content_type` (data type of the response), and `headers` (custom headers) separately.

## 4.3 Response — JSON Response

First, a quick review of the two basic operations of Python's standard `json` module:

```python
>>> data = {'name': '阿白'}
>>> import json

>>> json_string = json.dumps(data)
>>> json_string
'{"name": "\\u963f\\u767d"}'

>>> json_data = json.loads(json_string)
>>> json_data
{'name': '阿白'}
```

- `json.dumps()`: converts a Python object into a JSON string (by default, Chinese characters are escaped as `\uXXXX` sequences);
- `json.loads()`: parses a JSON string back into a Python object.

There are two ways to build a JSON response in Flask.

**Option 1: `jsonify`**

`jsonify` is Flask's built-in helper that builds a JSON response object directly; the returned response object can be further manipulated:

```python
from flask import Flask, jsonify

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # return directly
    # return jsonify({'name': '阿白'})

    # or build the response object first, then return it
    json_response = jsonify({'name': '阿白'})
    return json_response
```

**Option 2: via `make_response`**

```python
from flask import Flask, make_response
import json

app = Flask(__name__)

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # - build the response object
    response = make_response()
    # - set the response header -- data type Content-Type: application/json; charset=utf-8
    # note: the ; must be a half-width (English) semicolon
    response.headers['Content-Type'] = 'application/json; charset=utf-8'

    # - build the response data: a JSON string
    data = {'name': '阿白'}
    # the dumps function of the json module converts json to a json string
    json_data_string = json.dumps(data)

    response.data = json_data_string

    return response

if __name__ == '__main__':
    print(app.url_map)  # view routing info
    app.run(debug=True)
```

Key points:

- `jsonify` automatically serializes the data to JSON and sets the correct `Content-Type` — it is the most convenient option;
- The manual approach takes three steps: build the response object → set the header `Content-Type: application/json; charset=utf-8` → convert the data to a JSON string with `json.dumps()` and assign it to `response.data`.

[← Previous: Routing and Requests](03-routing-and-requests.md) | [Next: Responses →](05-responses.md)
