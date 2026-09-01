[← Previous: Account Management](14-account-management.md) | [Next: Member Management →](16-member-management.md)

# 15 Log Management

The admin backend needs to record two kinds of runtime logs: **access logs** (the request details of every successful visit) and **error logs** (details of failed requests such as 404s). This chapter implements both on the Flask backend: generate model classes from the existing tables with `flask-sqlacodegen`, build a unified `LogService`, write logs automatically via an interceptor and an error-handling hook, and finally display a user's recent access history on the account detail page.

## 15.1 Generating Log Models from Tables

Log data is stored in two tables of the `food_db` database: `app_access_log` (access logs) and `app_error_log` (error logs). `flask-sqlacodegen` can generate the corresponding model classes directly from the table structures.

Install the package (skip if already installed):

```bash
pip install flask-sqlacodegen
```

Following the same approach used to generate the User model class, generate the two log model classes. **Note: do not rebuild SQLAlchemy.** The two generation commands are:

```bash
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables app_access_log --outfile "web/models/AppAccessLog.py" --flask

flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables app_error_log --outfile "web/models/AppErrorLog.py" --flask
```

The two generated model files go into `web/models/` (alongside `user.py`). **Refactor the db import**: the import at the top of the generated code must be changed to the project's unified style:

```python
from application import db
```

## 15.2 Access Log Handling

### 15.2.1 Writing the LogService Module

Create a `LogService.py` module under `common/libs`, define the `LogService` class, and add a static method that records access logs:

```python
from flask import request, g
from application import db
from datetime import datetime
import json
from web.models.AppAccessLog import AppAccessLog


class LogService():
    @staticmethod
    def addAccesslog():
        """Add an access log entry to the database"""
        target = AppAccessLog()
        if "current_user" in g and g.current_user is not None:
            target.uid = g.current_user.uid  # uid of the current user
        target.referer_url = request.referrer
        target.target_url = request.url
        target.query_params = json.dumps(request.values.to_dict())
        target.ua = request.headers.get("User-Agent")
        target.created_time = datetime.now()
        # write to the database
        db.session.add(target)
        db.session.commit()
        return True
```

Field reference:

| Field | Meaning | Source |
| --- | --- | --- |
| `uid` | ID of the logged-in user | `g.current_user.uid` (omitted when not logged in) |
| `referer_url` | Referring page URL | `request.referrer` |
| `target_url` | URL being accessed | `request.url` |
| `query_params` | Request parameters (JSON string) | `json.dumps(request.values.to_dict())` |
| `ua` | Client User-Agent | `request.headers.get("User-Agent")` |
| `created_time` | Access time | `datetime.now()` |

### 15.2.2 Writing Access Logs in the Interceptor

In the `before_request()` function of the auth interceptor `web/interceptors/AuthInterceptor.py`, write the access log to the database before each request is served normally. After the login check passes (`g.current_user` is assigned), add:

```python
# write the log
from common.libs.LogService import LogService
LogService.addAccesslog()
```

Now every request that passes the interceptor's login verification automatically records one access log entry.

### 15.2.3 Passing the Log List in the info View of Account.py

In the `info` view method of the `Account.py` module, query the account's recent access logs and pass them to the page. On top of the existing user-info query, add:

```python
# from web.models.AppAccessLog import AppAccessLog

access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
context['access_list'] = access_list
```

This filters by `uid`, orders by id descending, and takes at most the 10 most recent access records.

### 15.2.4 Updating info.html to Show the Access History

Update the `account/info.html` page to display the personal access history list (access time and target URL) in the table:

```html
<tbody>
{% if access_list %}
    {% for item in access_list %}
    <tr>
        <td>{{ item.created_time }}</td>
        <td>{{ item.target_url }}</td>
    </tr>
    {% endfor %}
{% else %}
    <tr><td colspan="2">No data yet</td></tr>
{% endif %}
</tbody>
```

## 15.3 Error Log Handling

### 15.3.1 Adding the Error Log Method to LogService

Add a static method `addErrorlog` to the `LogService` class (the `AppErrorLog` model must be imported first):

```python
class LogService():

    @staticmethod
    def addErrorlog(content):
        """Add an error log entry to the database"""
        if "favicon.ico" in request.url:
            print("404 caused by the favicon can be ignored")
            return
        target = AppErrorLog()
        target.referer_url = request.referrer
        target.target_url = request.url
        target.query_params = json.dumps(request.values.to_dict())
        target.content = content
        target.created_time = datetime.now()
        # write to the database
        db.session.add(target)
        db.session.commit()
        print("written to the database successfully")
        return True
```

Key points:

- Browsers frequently trigger 404s by requesting `favicon.ico`; these are meaningless noise and are skipped instead of being written to the database.
- The `content` parameter stores the actual error details (the exception string passed in by the caller).

### 15.3.2 Creating the ErrorInterceptor

Create `ErrorInterceptor.py` under `web/interceptors/` to intercept 404 errors, write the error information to the log (database), and render a unified error page:

```python
from application import app
from common.libs.LogService import LogService
from common.libs.render_helper import ops_render


@app.errorhandler(404)
def error_404(e):
    LogService.addErrorlog(str(e))  # error content
    return ops_render("error/error.html",
                      {"msg": "Sorry, the page you visited does not exist~",
                       "status": 404
                       })
```

### 15.3.3 Loading the Interceptor in www.py

After creating the interceptor file, it must be imported in `www.py` so the hook function is attached to the application:

```python
from web.interceptors.AuthInterceptor import *
from web.interceptors.ErrorInterceptor import *
```

With this, the 404 error handler is registered when the app starts: any visit to a nonexistent page first writes an error log entry, then shows the user a friendly error page.

[← Previous: Account Management](14-account-management.md) | [Next: Member Management →](16-member-management.md)
