[← 上一篇：操作训练与蓝图](14-操作训练与蓝图.md) | [下一篇：RESTful →](16-RESTful.md)

# 15 蓝图与Flask-Mail

## 15.1 蓝图（Blueprint）——路由与端点

在中大型项目中，通常会按业务拆分模块（用户模块、权限模块、文件模块等），每个模块还涉及身份验证、安全校验等横切逻辑。当视图函数非常多的时候，路由管理就成了问题。编程开发讲究"高内聚、低耦合"，Flask 提供的**蓝图（Blueprint）**就是用来对视图函数进行结构化管理的机制。

### 15.1.1 蓝图的基本使用

蓝图的实现分三步：

1. 先生成蓝图对象（`from flask import Blueprint`）；
2. 通过蓝图对象注册视图函数；
3. 最后将蓝图对象汇集注册到 Flask 应用实例对象。

```python
from flask import Flask
from apps.index import app_index
from apps.file import app_file
from apps.user import app_user
from apps.users.demo import app_study

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

# 注册——将蓝图对象汇集注册到flask应用实例对象
app.register_blueprint(app_file, url_prefix='/app_file')
app.register_blueprint(app_index)
app.register_blueprint(app_user)
app.register_blueprint(app_study)

if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

注册后 `app.url_map` 中可以看到类似这样的路由：

```text
Map([<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/app_file/file' (HEAD, GET, OPTIONS) -> app_file.file>,
 <Rule '/index' (HEAD, GET, OPTIONS) -> app_index.file>,
 <Rule '/user' (HEAD, GET, OPTIONS) -> app_user.file>,
 <Rule '/study' (HEAD, GET, OPTIONS) -> app_study.file>])
```

### 15.1.2 蓝图注册的内部过程

`@蓝图对象.route` 装饰视图函数时，**并没有在应用对象中注册路由，也没有改变 `app.url_map`**。它只是向蓝图实例对象的 `deferred_functions` 列表中添加了一段"路由信息函数"：

- `name='app_file'`：蓝图名称
- `deferred_functions=[函数1, 函数2, ...]`：延迟执行的路由注册函数列表

当调用 `应用实例对象.register_blueprint(蓝图对象)` 时：

1. 遍历蓝图对象的 `deferred_functions` 列表，取出路由信息函数；
2. 调用路由信息函数，内部执行 `add_url_rule`；
3. 结合注册时蓝图提供的 `url_prefix` 和蓝图内部路由，生成最终路由。

例如：

```python
app.register_blueprint(app_file, url_prefix='/app_file')

# 蓝图内部：
# @app_file.route('/file', methods=['GET'])
```

最终生成的路由是 `/app_file/file`，即：

```text
<Rule '/app_file/file' (OPTIONS, HEAD, GET) -> app_file.file>
```

### 15.1.3 端点 endpoint 的命名规则

路由信息中的端点（endpoint）为 `app_file.file`，由两部分组成：

- `app_file`：蓝图名称
- `file`：视图端点名称，默认就是视图函数名

因此，在蓝图中使用 `url_for` 反向解析 URL 时，端点要带上蓝图名称：

```python
print(url_for('app_file.file'))  # /app_file/file
```

## 15.2 蓝图资源管理问题

蓝图除了管理视图函数，还可以拥有自己的模板目录和静态资源目录。

### 15.2.1 蓝图的模板目录

创建蓝图对象时可以通过 `template_folder` 指定蓝图自己的模板目录：

```python
from flask import Blueprint, render_template

app_study = Blueprint('app_study', __name__,
                      template_folder="study_templates")

@app_study.route('/study', methods=['GET'])
def study():
    # 找模板的顺序：主模板目录（应用对象中注册的template_folder）
    #              ---> 子模板目录（蓝图对象中注册的template_folder）
    return render_template('demo1.html')
```

**模板查找顺序**：先找主模板目录（应用对象中注册的 `template_folder`），找不到再找子模板目录（蓝图对象中注册的 `template_folder`）。因此如果主模板目录和蓝图模板目录中存在同名模板，主目录的模板会优先被使用。

### 15.2.2 蓝图的静态资源目录

蓝图同样可以指定自己的静态资源目录：

```python
from flask import Blueprint, render_template

app_study = Blueprint('app_study', __name__,
                      template_folder="study_templates",
                      static_folder="study_static",
                      static_url_path='/study_static')
# static_url_path前缀名 默认为：/ + static_folder值

@app_study.route('/study', methods=['GET'])
def study():
    return render_template('demo1.html')
```

- `static_folder`：蓝图静态资源的实际目录；
- `static_url_path`：静态资源的 URL 前缀，默认为 `/` + `static_folder` 的值。

注册后 `app.url_map` 中会多出一条蓝图静态资源路由：

```text
<Rule '/study_static/<filename>' (HEAD, OPTIONS, GET) -> app_study.static>
```

![[ch15-blueprint-resources.png]]

**注意静态资源的匹配陷阱**：请求会先匹配主路由的静态资源路径，匹配不到就直接报 404。如果子路由（蓝图）的静态资源路径与主路由的静态资源路径一样（例如都叫 `/static`），访问不到子路由的静态资源——所以蓝图的 `static_url_path` 应与主应用的区分开。

## 15.3 Flask-Mail 邮件扩展

### 15.3.1 安装

```bash
pip install Flask-Mail
```

### 15.3.2 邮件协议基础

邮件收发涉及三个常见协议，以 163 邮箱为例（<https://email.163.com/>，设置中开启 POP3/SMTP/IMAP 服务）：

**SMTP（Simple Mail Transfer Protocol）**

SMTP 是用于发送邮件的协议。它规定了邮件从源地址到目的地址的传输规范，控制邮件的中转方式。SMTP 服务器遵循 SMTP 协议，负责发送邮件。SMTP 是一个"推"协议，不支持从远程服务器上"拉"取消息。SMTP 认证要求提供账户名和密码才能登录 SMTP 服务器，这有助于避免垃圾邮件的侵扰。

**POP3（Post Office Protocol 3）**

POP3 是邮局协议的第三个版本，主要用于支持客户端远程管理服务器上的电子邮件。它允许用户将邮件从服务器下载到本地主机，并删除服务器上的邮件。POP3 服务器是遵循 POP3 协议的接收邮件服务器，用于接收电子邮件。

**IMAP（Internet Mail Access Protocol）**

IMAP 是交互式邮件存取协议，允许用户从本地邮件客户端访问远程服务器上的邮件。与 POP3 不同，IMAP 在客户端收取邮件后仍然保留邮件在服务器上，客户端上的操作（如删除邮件、标记已读）会反馈到服务器上，实现邮件状态的同步。

**区别与联系**：

- POP3 允许电子邮件客户端下载服务器上的邮件，但客户端的操作不会反馈到服务器上。这意味着，如果通过客户端收取邮件并进行操作（如移动邮件），服务器上的邮件不会同步移动。
- IMAP 提供了与 POP3 类似的邮件下载服务，但同时支持邮件状态的双向同步。用户可以在多个设备上访问新邮件，并且邮件状态在各个设备上保持一致。
- SMTP 则专注于邮件的发送，不涉及邮件的接收和状态同步。

| 协议 | 功能 | 端口 | 加密端口 | 特点 |
| --- | --- | --- | --- | --- |
| SMTP | 发送邮件 | 25 | 587 | 简单易用，广泛支持，无状态，用于邮件发送 |
| POP3 | 接收邮件（下载到本地） | 110 | 995 | 简单高效，适合离线使用，不支持文件夹管理，邮件下载后通常从服务器删除 |
| IMAP | 接收邮件（服务器管理） | 143 | 993 | 支持文件夹管理，多设备同步，支持部分下载，邮件保留在服务器上 |

### 15.3.3 163 邮箱开启 SMTP 服务

这里使用 163 邮箱做演示。注册好 163 邮箱后，需要将 SMTP 协议开启，才能通过第三方客户端登录：

1. 登录 <https://email.163.com/>，在设置中找到 POP3/SMTP/IMAP 选项；
2. 在新页面中点击开启，弹出新窗口填写手机验证码；
3. 开启后会获得一个**授权码**（不是邮箱登录密码），代码中的 `MAIL_PASSWORD` 填的就是这个授权码。

### 15.3.4 配置并发送邮件

```python
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__,
            template_folder='templates')

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.163.com',  # 邮箱的smtp服务器
    MAIL_PORT=25,                # 邮件的服务器端口
    MAIL_USE_TLS=True,           # 使用tls安全协议
    MAIL_USERNAME='',            # 你的邮箱
    MAIL_PASSWORD=''             # 你的授权码
)

mail = Mail(app)

@app.route('/')
def index():
    """
    subject: 邮件标题,
    recipients: 接收方列表，如果是多个接收方，那就是群发,
    body: 邮件正文,
    html: 网页形式的正文,
    sender: 发送方,
    cc: 抄送列表,
    bcc: 密件抄送,
    attachments: 附件实例列表,
    """
    msg = Message(
        subject='测试邮件发送功能',
        sender=app.config['MAIL_USERNAME'],
        recipients=[''],  # 接收方的邮件
        cc=[app.config['MAIL_USERNAME']]
    )
    msg.html = '<h2 style="color:red">flask-mail</h2>'

    # 添加附件        文件名          文件类型            文件数据
    msg.attach(filename='01.png', content_type='image/png', data=open('01.png', 'rb').read())

    # 发送邮件
    mail.send(msg)

    return '发送成功'

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```

### 15.3.5 端口与加密协议问题排查

使用 25 端口 + TLS 配置时，可能遇到两类报错：

**报错一：连接被断开**——`smtplib.SMTPServerDisconnected: Connection unexpectedly closed`

![[ch15-smtp-server-disconnected.png]]

**报错二：切换到 465 端口后仍开启 TLS**——`smtplib.SMTPResponseException: (454, b'Command not permitted when TLS active')`

![[ch15-smtp-tls-error.png]]

解决办法：**打开 SSL 配置，关闭 TLS 配置，使用 465 端口**，即可发送成功：

```python
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.163.com',  # 邮箱的smtp服务器
    MAIL_PORT=465,               # 邮件的服务器端口
    # MAIL_USE_TLS=True,         # 使用tls安全协议——465端口下需关闭
    MAIL_USERNAME='',            # 你的邮箱
    MAIL_PASSWORD='',            # 你的授权码
    MAIL_USE_SSL=True            # 使用ssl安全协议
)
```

[← 上一篇：操作训练与蓝图](14-操作训练与蓝图.md) | [下一篇：RESTful →](16-RESTful.md)
