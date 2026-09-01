[← 上一篇：蓝图与Flask-Mail](15-蓝图与Flask-Mail.md) | [下一篇：二手房项目简介 →](17-二手房项目简介.md)

# 16 RESTful

## 16.1 REST API 概念

REST API 是开发的一套**规范标准**，用于前后端之间的数据交互：

- 直接通过 HTTP，不需要额外的协议：使用 `post`、`get`、`put`、`delete` 等标准方法
- 一目了然，具有自解释性
- 数据描述：通常是 `json` / `xml`

**核心思想：用 HTTP 标准方法表示增删改查，URL 代表资源。**

规范示例：同一个 URL，用不同的 HTTP 方法表示不同的操作。

```
/api/user  --GET-->  get 方法处理 get 请求   ---> 返回相应数据
/api/user  --POST--> post 方法处理 post 请求 ---> 返回相应数据
```

### 16.1.1 REST 的含义

```
REST = Representational State Transfer
       表现层状态转化
```

- 「表现层」指的是**资源的表现层**。
- URL 应该只表示资源的位置，而不是资源的具体表现形式。例如：

```
https://cn.bing.com/search        ---> 资源的表现层
https://cn.bing.com/search.html   ---> 资源位置 + 表现形式（不符合 REST 风格）
```

### 16.1.2 URI 与 URL

- **URI** 是一个更广泛的概念，它是用来**唯一标识**一个资源的字符串。这个资源可以是网络上的一个页面、一个服务、一个文件等。URI 的存在就是为了能够让我们通过一个**独特的标识**来找到这个资源。例如，一个人的身份证号码就可以被视为一个 URI，因为它能够唯一标识一个人。
- **URL** 则是 URI 的一个子集，它不仅唯一标识一个资源，还提供了如何定位这个资源的方法。URL 包含了访问资源所需的所有信息，包括协议、域名、端口、路径等。例如，`http://www.example.com/index.html` 是一个 URL，它指明了通过 HTTP 协议访问 `www.example.com` 域名下的 `index.html` 页面。

简单区分：

- **URL 的作用**：URL 通常是一个完整的链接，用户可以直接通过这个链接访问网站。例如，将 URL 复制到浏览器中即可访问相应的网站。
- **URI 的作用**：URI 更多用于编程中，作为相对地址使用。例如，在编程时可以使用 `request.getRequestURI` 来获取页面的相对地址，而不需要每次都使用绝对 URL。

### 16.1.3 RESTful API 的核心作用

1. **前后端分离解耦**：后端只提供数据接口，不渲染页面；前端（管理后台、微信小程序）独立写界面，双方只通过 JSON 通信。
2. **多端复用一套接口**：管理网页、司机小程序、车辆终端 APP，全部调用同一套 REST 接口，不用重复写多套逻辑。
3. **标准化数据交互**：统一返回 JSON 格式，约定状态码、错误信息，任何人调用都看得懂。
4. **轻量化数据传输**：只传 JSON 纯数据，不像传统页面返回完整 HTML，网络流量更小、响应更快。
5. **便于第三方对接**：后续如果要对接车载设备、第三方调度系统，直接调用 REST 接口即可。

## 16.2 使用 RESTful API（flask-restful）

Flask 中通过 `flask-restful` 扩展来实现 RESTful API：

```shell
pip install flask-restful
```

### 16.2.1 基本用法

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

api = Api(app)  # restful api 挂载到应用的实例对象上


class Helloworld(Resource):  # 定义类视图 --> 继承 Resource
    # 对象方法，必须接受 self
    def get(self):  # 定义 get 方法 ---> 处理 get 请求
        print(self)
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# 注册类视图
# api.add_resource(Helloworld, '/')
# api.add_resource(Helloworld, '/', '/index')
# api.add_resource(Helloworld, '/', '/index', endpoint='index')
api.add_resource(Helloworld, '/', '/index')

if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

`add_resource` 的参数说明：

| 参数 | 说明 |
| --- | --- |
| `resource` | 要注册的 Resource 类（资源类） |
| `*urls` | 路由，可以传多个路由 |
| `endpoint` | 端点，默认是资源类名称的小写版 |

上面几种注册方式对应的路由信息（`app.url_map`）如下：

```python
# 只注册 '/'：endpoint 默认为类名小写 helloworld
Map([<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/' (HEAD, GET, OPTIONS) -> helloworld>])

# 类中同时定义了 get 和 post 方法后，路由支持的方法随之增加
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 <Rule '/' (OPTIONS, POST, GET, HEAD) -> helloworld>])

# 注册多个路由 '/' 和 '/index'，指向同一个资源类
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 <Rule '/' (OPTIONS, GET, HEAD, POST) -> helloworld>,
 <Rule '/index' (OPTIONS, GET, HEAD, POST) -> helloworld>])

# 指定 endpoint='index' 后，端点名称变为 index
Map([<Rule '/static/<filename>' (OPTIONS, HEAD, GET) -> static>,
 <Rule '/' (POST, OPTIONS, HEAD, GET) -> index>,
 <Rule '/index' (POST, OPTIONS, HEAD, GET) -> index>])
```

### 16.2.2 路由中携带参数

路由中的参数会作为对象方法的参数传入，方法定义时需要接收对应的形参：

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

api = Api(app)  # restful api 挂载到应用的实例对象上


class Helloworld(Resource):  # 定义类视图 --> 继承 Resource
    # 对象方法，必须接受 self
    def get(self, name):  # 定义 get 方法 --> 处理 get 请求
        print(name)
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# 注册类视图
api.add_resource(Helloworld, '/index/<name>/')

if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

## 16.3 蓝图与类视图结合

`Api` 对象也可以挂载到蓝图对象上，形成「api 蓝图对象」，再将蓝图注册到应用实例中：

```python
from flask import Flask, Blueprint
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

app_hello = Blueprint('app_hello', __name__)  # 生成蓝图对象
api_hello = Api(app_hello)  # api 挂载蓝图对象 ---> api 蓝图对象


class Helloworld(Resource):  # 定义类视图 --> 继承 Resource
    # 对象方法，必须接受 self
    def get(self):  # 定义 get 方法 ---> 处理 get 请求
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# 注册
api_hello.add_resource(Helloworld, '/')  # api 蓝图对象注册资源类

app.register_blueprint(app_hello)  # 将 api 蓝图对象注册到 app 应用实例对象里面去

"""
路由信息：端点带有蓝图名前缀 app_hello.
Map([<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/' (HEAD, POST, GET, OPTIONS) -> app_hello.helloworld>])
"""

if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

## 16.4 类视图与装饰器

### 16.4.1 解决 JSON 中文编码问题

返回包含中文的 JSON 数据时，需要关闭 ASCII 转义：

```python
# 解决 json 中文编码问题
app.config['JSON_AS_ASCII'] = False
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
```

### 16.4.2 method_decorators 给类视图方法添加装饰器

类视图中不能直接给方法加 `@装饰器`（因为方法必须接受 `self`），而是通过类属性 `method_decorators` 指定：键是请求方法名（如 `'get'`），值是装饰器列表。

```python
from flask import Flask, Blueprint
from flask_restful import Api, Resource

app = Flask(__name__, template_folder='templates')

# 解决 json 中文编码问题
app.config['JSON_AS_ASCII'] = False
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

api = Api(app)


def decorator2(func):  # func 被装饰函数
    def wrapper(*args, **kwargs):  # 接受函数参数 ---> 不定长
        print("装饰器2 -- start")
        data = func(*args, **kwargs)
        print("装饰器2 -- end")
        return data
    return wrapper


def decorator1(func):  # func 被装饰函数
    def wrapper(*args, **kwargs):  # 接受函数参数 ---> 不定长
        print("装饰器1 -- start")
        data = func(*args, **kwargs)
        print("装饰器1 -- end")
        return data
    return wrapper


class Helloworld(Resource):  # 定义类视图 --> 继承 Resource

    method_decorators = {
        'get': [decorator2, decorator1],
    }

    # 对象方法，必须接受 self
    def get(self):  # 定义 get 方法 ---> 处理 get 请求
        print("-----  视图  ------")
        return {'content': 'GET请求响应'}

    def post(self):
        return {'content': 'POST请求响应'}


# 注册
api.add_resource(Helloworld, '/')

if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

装饰器的挂载与执行顺序——**先入后出**：

```
挂载装饰器的时候：  方法 ----》 decorator2 ----》 decorator1

执行：  请求 ---》 decorator1 -请求-》 decorator2 -请求-》 方法
        方法 -响应-》 decorator2 -响应-》 decorator1 ---> 响应
```

实际输出：

```
装饰器1 -- start
装饰器2 -- start
-----  视图  ------
装饰器2 -- end
装饰器1 -- end
```

即：列表中越靠后的装饰器越靠近视图方法；请求进入时从外层（列表末尾的装饰器）开始执行，响应返回时从内向外依次结束。

[← 上一篇：蓝图与Flask-Mail](15-蓝图与Flask-Mail.md) | [下一篇：二手房项目简介 →](17-二手房项目简介.md)
