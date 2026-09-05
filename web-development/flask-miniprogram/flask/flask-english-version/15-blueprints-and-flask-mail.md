[← Previous: Practice Exercises and Blueprints](14-exercises-and-blueprints.md) | [Next: RESTful →](16-restful.md)

# 15 Blueprints and Flask-Mail

## 15.1 Blueprints — Routes and Endpoints

In medium-to-large projects, the code is usually split into business modules (user module, permission module, file module, etc.), and each module may involve cross-cutting concerns such as authentication and security checks. When there are many view functions, route management becomes a problem. Programming favors "high cohesion and low coupling", and Flask's **Blueprint** is the mechanism for structuring and organizing view functions.

### 15.1.1 Basic Usage of Blueprints

Using a blueprint takes three steps:

1. Create a blueprint object (`from flask import Blueprint`);
2. Register view functions on the blueprint object;
3. Finally register the blueprint objects onto the Flask application instance.

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

# Register — collect the blueprint objects onto the Flask application instance
app.register_blueprint(app_file, url_prefix='/app_file')
app.register_blueprint(app_index)
app.register_blueprint(app_user)
app.register_blueprint(app_study)

if __name__ == '__main__':
    print(app.url_map)  # inspect the route table
    app.run(debug=True)
```

After registration, `app.url_map` contains routes like these:

```text
Map([<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/app_file/file' (HEAD, GET, OPTIONS) -> app_file.file>,
 <Rule '/index' (HEAD, GET, OPTIONS) -> app_index.file>,
 <Rule '/user' (HEAD, GET, OPTIONS) -> app_user.file>,
 <Rule '/study' (HEAD, GET, OPTIONS) -> app_study.file>])
```

### 15.1.2 The Internal Registration Process

When `@blueprint.route` decorates a view function, **the route is NOT registered on the application object, and `app.url_map` is NOT changed**. It merely appends a "route-information function" to the blueprint instance's `deferred_functions` list:

- `name='app_file'`: the blueprint name
- `deferred_functions=[func1, func2, ...]`: the list of deferred route-registration functions

When `app.register_blueprint(blueprint)` is called:

1. It iterates over the blueprint's `deferred_functions` list and takes out each route-information function;
2. It invokes the route-information function, which internally calls `add_url_rule`;
3. It combines the `url_prefix` provided at registration time with the blueprint's internal route to produce the final route.

For example:

```python
app.register_blueprint(app_file, url_prefix='/app_file')

# Inside the blueprint:
# @app_file.route('/file', methods=['GET'])
```

The final route is `/app_file/file`:

```text
<Rule '/app_file/file' (OPTIONS, HEAD, GET) -> app_file.file>
```

### 15.1.3 Endpoint Naming Rules

The endpoint in the route information is `app_file.file`, which consists of two parts:

- `app_file`: the blueprint name
- `file`: the view endpoint name, which defaults to the view function name

Therefore, when reversing a URL with `url_for` inside a blueprint, the endpoint must include the blueprint name:

```python
print(url_for('app_file.file'))  # /app_file/file
```

## 15.2 Blueprint Resource Management

Besides organizing view functions, a blueprint can also have its own template folder and static folder.

### 15.2.1 Blueprint Template Folder

When creating a blueprint object, you can specify its own template folder with `template_folder`:

```python
from flask import Blueprint, render_template

app_study = Blueprint('app_study', __name__,
                      template_folder="study_templates")

@app_study.route('/study', methods=['GET'])
def study():
    # Template lookup order: main template folder (the template_folder
    # registered on the app) ---> blueprint template folder (the
    # template_folder registered on the blueprint)
    return render_template('demo1.html')
```

**Template lookup order**: the main template folder (the `template_folder` registered on the application object) is searched first; if not found, the blueprint's template folder (the `template_folder` registered on the blueprint object) is searched. So if a template with the same name exists in both the main folder and the blueprint folder, the one in the main folder wins.

### 15.2.2 Blueprint Static Folder

A blueprint can also specify its own static folder:

```python
from flask import Blueprint, render_template

app_study = Blueprint('app_study', __name__,
                      template_folder="study_templates",
                      static_folder="study_static",
                      static_url_path='/study_static')
# static_url_path defaults to "/" + the static_folder value

@app_study.route('/study', methods=['GET'])
def study():
    return render_template('demo1.html')
```

- `static_folder`: the blueprint's actual static resource directory;
- `static_url_path`: the URL prefix of the static resources, defaulting to `/` + the value of `static_folder`.

After registration, `app.url_map` gains an extra static route for the blueprint:

```text
<Rule '/study_static/<filename>' (HEAD, OPTIONS, GET) -> app_study.static>
```

![[ch15-blueprint-resources.png]]

**Beware of the static-matching trap**: a request first matches the main app's static route, and if nothing matches it returns 404 directly. If the blueprint's static URL path is the same as the main app's (e.g. both are `/static`), the blueprint's static resources become unreachable — so the blueprint's `static_url_path` should be different from the main app's.

## 15.3 The Flask-Mail Extension

### 15.3.1 Installation

```bash
pip install Flask-Mail
```

### 15.3.2 Email Protocol Basics

Sending and receiving email involves three common protocols. Take the 163 mailbox as an example (<https://email.163.com/>, enable the POP3/SMTP/IMAP service in settings):

**SMTP (Simple Mail Transfer Protocol)**

SMTP is the protocol used to send email. It defines the transmission rules for email from the source address to the destination address, and controls how messages are relayed. An SMTP server follows the SMTP protocol and is responsible for sending email. SMTP is a "push" protocol — it cannot "pull" messages from a remote server. SMTP authentication requires an account name and password to log in to the SMTP server, which helps prevent spam abuse.

**POP3 (Post Office Protocol 3)**

POP3 is the third version of the Post Office Protocol, mainly used to let a client remotely manage email on the server. It allows users to download email from the server to a local host and delete the email on the server. A POP3 server is an incoming mail server that follows the POP3 protocol and is used to receive email.

**IMAP (Internet Mail Access Protocol)**

IMAP is the Interactive Mail Access Protocol, which allows users to access email on a remote server from a local mail client. Unlike POP3, IMAP keeps email on the server after the client retrieves it, and operations on the client (such as deleting email or marking it as read) are fed back to the server, synchronizing the mail state.

**Differences and connections**:

- POP3 allows an email client to download email from the server, but operations on the client are not fed back to the server. This means that if you fetch email through the client and operate on it (such as moving a message), the email on the server is not moved accordingly.
- IMAP provides a download service similar to POP3, but also supports two-way synchronization of mail state. Users can access new email on multiple devices, and the mail state stays consistent across devices.
- SMTP focuses solely on sending email; it is not involved in receiving email or state synchronization.

| Protocol | Function | Port | Encrypted port | Characteristics |
| --- | --- | --- | --- | --- |
| SMTP | Sending email | 25 | 587 | Simple and easy to use, widely supported, stateless, used for sending email |
| POP3 | Receiving email (download to local) | 110 | 995 | Simple and efficient, good for offline use, no folder management, email is usually deleted from the server after download |
| IMAP | Receiving email (managed on the server) | 143 | 993 | Supports folder management, multi-device sync, partial download; email stays on the server |

### 15.3.3 Enabling SMTP on a 163 Mailbox

The demo uses a 163 mailbox. After registering a 163 mailbox, you must enable the SMTP protocol before a third-party client can log in:

1. Log in to <https://email.163.com/> and find the POP3/SMTP/IMAP option in settings;
2. Click "enable" on the new page, and fill in the SMS verification code in the pop-up window;
3. Once enabled you get an **authorization code** (not the mailbox login password) — this authorization code is what goes into `MAIL_PASSWORD` in the code.

### 15.3.4 Configuring and Sending Email

```python
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__,
            template_folder='templates')

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.163.com',  # the mailbox's SMTP server
    MAIL_PORT=25,                # the mail server port
    MAIL_USE_TLS=True,           # use the TLS security protocol
    MAIL_USERNAME='',            # your mailbox
    MAIL_PASSWORD=''             # your authorization code
)

mail = Mail(app)

@app.route('/')
def index():
    """
    subject: the email subject,
    recipients: the recipient list; multiple recipients means a mass mailing,
    body: the plain-text body,
    html: the HTML body,
    sender: the sender,
    cc: the CC list,
    bcc: the BCC list,
    attachments: the list of attachment instances,
    """
    msg = Message(
        subject='Test email sending',
        sender=app.config['MAIL_USERNAME'],
        recipients=[''],  # the recipient's email address
        cc=[app.config['MAIL_USERNAME']]
    )
    msg.html = '<h2 style="color:red">flask-mail</h2>'

    # Add an attachment:  filename     content type        file data
    msg.attach(filename='01.png', content_type='image/png', data=open('01.png', 'rb').read())

    # Send the email
    mail.send(msg)

    return 'Sent successfully'

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```

### 15.3.5 Troubleshooting Ports and Encryption Protocols

With port 25 + TLS, you may run into two kinds of errors:

**Error 1: connection dropped** — `smtplib.SMTPServerDisconnected: Connection unexpectedly closed`

![[ch15-smtp-server-disconnected.png]]

**Error 2: TLS still enabled after switching to port 465** — `smtplib.SMTPResponseException: (454, b'Command not permitted when TLS active')`

![[ch15-smtp-tls-error.png]]

The fix: **enable SSL, disable TLS, and use port 465** — then sending succeeds:

```python
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.163.com',  # the mailbox's SMTP server
    MAIL_PORT=465,               # the mail server port
    # MAIL_USE_TLS=True,         # TLS must be disabled on port 465
    MAIL_USERNAME='',            # your mailbox
    MAIL_PASSWORD='',            # your authorization code
    MAIL_USE_SSL=True            # use the SSL security protocol
)
```

[← Previous: Practice Exercises and Blueprints](14-exercises-and-blueprints.md) | [Next: RESTful →](16-restful.md)
