[← Previous: Blueprints and Flask-Mail](15-blueprints-and-flask-mail.md) | [Next: Second-Hand Housing Project Introduction →](17-second-hand-housing-project-intro.md)

# 16 RESTful

## 16.1 REST API Concepts

A REST API is a set of **design conventions** for data exchange between the frontend and the backend:

- Works directly over HTTP, no extra protocol needed: uses standard methods such as `post`, `get`, `put`, and `delete`
- Clear at a glance, self-explanatory
- Data representation: usually `json` / `xml`

**Core idea: use standard HTTP methods to express CRUD operations, and let the URL represent the resource.**

Convention example: the same URL, with different HTTP methods expressing different operations.

```
/api/user  --GET-->  the get method handles the get request   ---> returns the corresponding data
/api/user  --POST--> the post method handles the post request ---> returns the corresponding data
```

### 16.1.1 What REST Means

```
REST = Representational State Transfer
```

- The "representational layer" refers to the **representation of a resource**.
- A URL should indicate only the location of a resource, not its concrete representation. For example:

```
https://cn.bing.com/search        ---> the resource's representation
https://cn.bing.com/search.html   ---> resource location + representation (not REST-style)
```

### 16.1.2 URI vs URL

- A **URI** is the broader concept: a string used to **uniquely identify** a resource. The resource can be a web page, a service, a file, and so on. A URI exists so that we can locate a resource through a **unique identifier**. For example, a person's national ID number can be seen as a URI, because it uniquely identifies one person.
- A **URL** is a subset of URI. It not only uniquely identifies a resource, but also tells you how to locate it. A URL contains all the information needed to access the resource, including the protocol, domain name, port, path, etc. For example, `http://www.example.com/index.html` is a URL: it specifies accessing the `index.html` page under the domain `www.example.com` over HTTP.

A simple way to tell them apart:

- **Role of a URL**: a URL is usually a complete link that users can use directly to visit a website. For example, copying the URL into a browser opens the corresponding site.
- **Role of a URI**: a URI is used more in programming, as a relative address. For example, in code you can use `request.getRequestURI` to get a page's relative address instead of always using an absolute URL.

### 16.1.3 Why Use a RESTful API

1. **Frontend/backend decoupling**: the backend only provides data interfaces and does not render pages; the frontend (admin console, WeChat mini-program) builds its own UI, and both sides communicate only through JSON.
2. **One set of interfaces reused by multiple clients**: the admin web page, driver mini-program, and vehicle terminal app all call the same REST interfaces — no need to write duplicate logic.
3. **Standardized data exchange**: responses uniformly use JSON, with agreed-upon status codes and error messages, so anyone can understand how to call them.
4. **Lightweight data transfer**: only pure JSON data is transferred, instead of full HTML pages, so traffic is smaller and responses are faster.
5. **Easy third-party integration**: to integrate vehicle-mounted devices or third-party dispatch systems later, they can simply call the REST interfaces.

## 16.2 Using RESTful APIs (flask-restful)

In Flask, RESTful APIs are implemented with the `flask-restful` extension:

```shell
pip install flask-restful
```

### 16.2.1 Basic Usage

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

api = Api(app)  # mount the restful api onto the application instance


class Helloworld(Resource):  # define a class-based view --> inherit from Resource
    # instance method, must accept self
    def get(self):  # define the get method ---> handles get requests
        print(self)
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# register the class-based view
# api.add_resource(Helloworld, '/')
# api.add_resource(Helloworld, '/', '/index')
# api.add_resource(Helloworld, '/', '/index', endpoint='index')
api.add_resource(Helloworld, '/', '/index')

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

Parameters of `add_resource`:

| Parameter | Description |
| --- | --- |
| `resource` | the Resource class to register (the resource) |
| `*urls` | routes; multiple routes can be passed |
| `endpoint` | the endpoint; defaults to the lowercase resource class name |

The routing tables (`app.url_map`) produced by the registration variants above:

```python
# registering only '/': the endpoint defaults to the lowercase class name helloworld
Map([<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/' (HEAD, GET, OPTIONS) -> helloworld>])

# after both get and post are defined in the class, the route supports more methods
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 <Rule '/' (OPTIONS, POST, GET, HEAD) -> helloworld>])

# registering multiple routes '/' and '/index' pointing to the same resource class
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 <Rule '/' (OPTIONS, GET, HEAD, POST) -> helloworld>,
 <Rule '/index' (OPTIONS, GET, HEAD, POST) -> helloworld>])

# with endpoint='index' specified, the endpoint name becomes index
Map([<Rule '/static/<filename>' (OPTIONS, HEAD, GET) -> static>,
 <Rule '/' (POST, OPTIONS, HEAD, GET) -> index>,
 <Rule '/index' (POST, OPTIONS, HEAD, GET) -> index>])
```

### 16.2.2 Parameters in Routes

Route parameters are passed into the resource methods as arguments, so the method must declare the corresponding parameters:

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

api = Api(app)  # mount the restful api onto the application instance


class Helloworld(Resource):  # define a class-based view --> inherit from Resource
    # instance method, must accept self
    def get(self, name):  # define the get method --> handles get requests
        print(name)
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# register the class-based view
api.add_resource(Helloworld, '/index/<name>/')

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

## 16.3 Combining Blueprints with Class-Based Views

An `Api` object can also be mounted onto a blueprint, creating an "API blueprint object", which is then registered on the application instance:

```python
from flask import Flask, Blueprint
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

app_hello = Blueprint('app_hello', __name__)  # create the blueprint object
api_hello = Api(app_hello)  # mount the api onto the blueprint ---> api blueprint object


class Helloworld(Resource):  # define a class-based view --> inherit from Resource
    # instance method, must accept self
    def get(self):  # define the get method ---> handles get requests
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# register
api_hello.add_resource(Helloworld, '/')  # register the resource class on the api blueprint object

app.register_blueprint(app_hello)  # register the api blueprint object onto the app instance

"""
Routing table: the endpoint carries the blueprint name prefix app_hello.
Map([<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/' (HEAD, POST, GET, OPTIONS) -> app_hello.helloworld>])
"""

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

## 16.4 Class-Based Views and Decorators

### 16.4.1 Fixing Chinese Character Encoding in JSON

When returning JSON data containing Chinese characters, ASCII escaping must be disabled:

```python
# fix Chinese character encoding in JSON
app.config['JSON_AS_ASCII'] = False
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
```

### 16.4.2 Adding Decorators to View Methods with method_decorators

You cannot apply `@decorator` directly to resource methods (they must accept `self`). Instead, use the class attribute `method_decorators`: the key is the request method name (e.g. `'get'`) and the value is a list of decorators.

```python
from flask import Flask, Blueprint
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

# fix Chinese character encoding in JSON
app.config['JSON_AS_ASCII'] = False
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

api = Api(app)


def decorator2(func):  # func is the decorated function
    def wrapper(*args, **kwargs):  # accept function arguments ---> variable-length
        print("装饰器2 -- start")
        data = func(*args, **kwargs)
        print("装饰器2 -- end")
        return data
    return wrapper


def decorator1(func):  # func is the decorated function
    def wrapper(*args, **kwargs):  # accept function arguments ---> variable-length
        print("装饰器1 -- start")
        data = func(*args, **kwargs)
        print("装饰器1 -- end")
        return data
    return wrapper


class Helloworld(Resource):  # define a class-based view --> inherit from Resource

    method_decorators = {
        'get': [decorator2, decorator1],
    }

    # instance method, must accept self
    def get(self):  # define the get method ---> handles get requests
        print("-----  view  ------")
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# register
api.add_resource(Helloworld, '/')

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

The order in which decorators are applied and executed — **first in, last out**:

```
When applying decorators:  method ----》 decorator2 ----》 decorator1

Execution:  request ---》 decorator1 -request-》 decorator2 -request-》 method
            method -response-》 decorator2 -response-》 decorator1 ---> response
```

Actual output:

```
装饰器1 -- start
装饰器2 -- start
-----  view  ------
装饰器2 -- end
装饰器1 -- end
```

In other words: the later a decorator appears in the list, the closer it wraps the view method; on the way in, execution starts from the outermost decorator (the last one in the list), and on the way out the decorators finish from the inside out.

[← Previous: Blueprints and Flask-Mail](15-blueprints-and-flask-mail.md) | [Next: Second-Hand Housing Project Introduction →](17-second-hand-housing-project-intro.md)
