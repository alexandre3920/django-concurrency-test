# Django concurrency test


## Description
[![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)](https://www.python.org/downloads/release/python-37/) [![Django 3.0](https://img.shields.io/badge/django-3.0-blue.svg)](https://docs.djangoproject.com/en/3.0/releases/3.0/)

This project is a Django application to test the concurrency error when saving objects. The test shows that in certain conditions, I encounter concurrency errors when saving objects. These errors occurs when the user *double-post* his form.
There errors is applicable to both `sqlite` and `posgresql` databases.
Of course there is very low probability for this kind of error to occur. Only user who *double-click* the submit button (even not on purpose) may raise this error.

This project is inspired by a *real* Django project I'm working on but I can't really share the full code :/ That's the reason why you may see in one of my view `PatientSignupView` a call to a Celery task which is not present in this project. I let the code as comment to show what the view is fully doing.


## Disclaimer :)
1. This project is made only to test the concurrency error,
2. I'm neither a `python` or a `bash` expert, so you may see some errors in my code :P.

## Workaround
In order to prevent the error, in this project I put in place a workaround with Javascript. When a form is submitted, the submit button is desactivated with Javascript. so if you try to reproduce the *double-post* from your browser, you may not be able to *double-click* the submit button.

## Install the project
I highly recommand using a virtualenv. I do use pyenv for this project.

1. First, install the requirements

```
pip install -r requirements/development.txt
```

2. Then apply the migrations

```
python manage.py migrate
```

3. And finaly create a superuser

You will need further an access to the Django Admin, therefor you need a superuser.
```
python manage.py createsuperuser
```

Note : note the email and the password you set, you need them to configure the scripts later

## Architecture
In a nutshell, this project is composed of:
- one app named `main`,
- one `DashboardUser` model which is set in the base.py settings as the `AUTH_USER_MODEL`,
  - the `DashboardUser` is a custom model (subclass of `AbstractBaseUser`) with an `email` field. The `USERNAME_FIELD` is the `email` field.
- one `PatientUser`model which has a `user` field as a `ForeignKey` to `DashboardUser` model,
- one `index` view,
- one `PatientSignupView` which is used for user of the application to register by submitting a form with basic informations (first name, last name, age, email and password)

## Run the tests
I created 2 `python` scripts and 2 `bash` scripts to run the tests:
1. The [first python script](./http_create_user_requests.py) is used to do a `POST` request on the `PatientSignupView`
2. The [second python script](./http_create_user_admin_requests.py) is used to do a `POST` request on the admin `Create DashboardUser` view (**authentication is required**)
  - **/!\** Because authentication is required, you have to custom the script and the `ADMIN_CREDENTIALS_USERNAME` and `ADMIN_CREDENTIALS_PASSWORD` with the credentials you set when you create the superuser.
3. The [first bash script](./run_create_user.sh) is used to create two threads of the [first python script](./http_create_user_requests.py) and simulate concurrent `POST` (*double-post*)
4. The [second bash script](./run_create_user_admin.sh) is used to create two threads of the [second python script](./http_create_user_admin_requests.py) and simulate concurrent `POST` (*double-post*)


## Reproduce the error
### 1. With the custom `PatientSignupView` view

**/!\ Make sure there is not already in the database a `DashboardUser` with the submitted email**

Run the [first bash script](./run_create_user.sh):
```
./run_create_user.sh
```

The first call will create a `DashboardUser` without error, but the second call will raise an `IntegrityError`

```python
[25/Oct/2020 11:42:42] "GET / HTTP/1.1" 200 12849
[25/Oct/2020 11:42:42] "GET / HTTP/1.1" 200 12851
[25/Oct/2020 11:42:42] "GET /mon-compte/creer/patient/ HTTP/1.1" 200 19453
[25/Oct/2020 11:42:42] "GET /mon-compte/creer/patient/ HTTP/1.1" 200 19437
[25/Oct/2020 11:42:43] "POST /mon-compte/creer/patient/ HTTP/1.1" 302 0
[25/Oct/2020 11:42:43] "GET /mon-compte/creer/confirmation/ HTTP/1.1" 200 12784
Internal Server Error: /mon-compte/creer/patient/
Traceback (most recent call last):
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/sqlite3/base.py", line 396, in execute
    return Database.Cursor.execute(self, query, params)
sqlite3.IntegrityError: UNIQUE constraint failed: main_dashboarduser.email

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/core/handlers/exception.py", line 34, in inner
    response = get_response(request)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/core/handlers/base.py", line 115, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/core/handlers/base.py", line 113, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/views/generic/base.py", line 71, in view
    return self.dispatch(request, *args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/views/generic/base.py", line 97, in dispatch
    return handler(request, *args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/views/generic/edit.py", line 172, in post
    return super().post(request, *args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/views/generic/edit.py", line 142, in post
    return self.form_valid(form)
  File "/[...]/django-concurrency-test/apps/main/views.py", line 39, in form_valid
    user = form.save()
  File "/[...]/.pyenv/versions/3.7.7/lib/python3.7/contextlib.py", line 74, in inner
    return func(*args, **kwds)
  File "/[...]/django-concurrency-test/apps/main/forms/users.py", line 58, in save
user.save()
  File "/[...]/django-concurrency-test/apps/main/models/users.py", line 102, in save
    super(DashboardUser, self).save(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/auth/base_user.py", line 66, in save
    super().save(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 749, in save
    force_update=force_update, update_fields=update_fields)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 787, in save_base
    force_update, using, update_fields,
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 890, in _save_table
    results = self._do_insert(cls._base_manager, using, fields, returning_fields, raw)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 929, in _do_insert
    using=using, raw=raw,
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/manager.py", line 82, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/query.py", line 1204, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1394, in execute_sql
    cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/debug_toolbar/panels/sql/tracking.py", line 198, in execute
    return self._record(self.cursor.execute, sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/debug_toolbar/panels/sql/tracking.py", line 133, in _record
    return method(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 100, in execute
    return super().execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 68, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 77, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/sqlite3/base.py", line 396, in execute
    return Database.Cursor.execute(self, query, params)
django.db.utils.IntegrityError: UNIQUE constraint failed: main_dashboarduser.email
[25/Oct/2020 11:42:43] "POST /mon-compte/creer/patient/ HTTP/1.1" 500 218616
```

### 2. With the admin `Create DashboaurdUser` view

**/!\ Make sure there is not already in the database a `DashboardUser` with the submitted email**

Run the [second bash script](./run_create_user_admin.sh):
```
./run_create_user_admin.sh
```

The first call will create a `DashboardUser` without error, but the second call will raise an `OperationnalError`

```python
[25/Oct/2020 11:47:04] "GET /admin/login/ HTTP/1.1" 200 11475
[25/Oct/2020 11:47:04] "GET /admin/login/ HTTP/1.1" 200 11475
[25/Oct/2020 11:47:04] "POST /admin/login/ HTTP/1.1" 302 0
[25/Oct/2020 11:47:04] "GET / HTTP/1.1" 200 12847
[25/Oct/2020 11:47:04] "POST /admin/login/ HTTP/1.1" 302 0
[25/Oct/2020 11:47:04] "GET / HTTP/1.1" 200 12855
[25/Oct/2020 11:47:06] "GET /admin/main/dashboarduser/add/ HTTP/1.1" 200 23981
[25/Oct/2020 11:47:07] "GET /admin/main/dashboarduser/add/ HTTP/1.1" 200 23979
Internal Server Error: /admin/main/dashboarduser/add/
Traceback (most recent call last):
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/sqlite3/base.py", line 396, in execute
    return Database.Cursor.execute(self, query, params)
sqlite3.OperationalError: database is locked

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/core/handlers/exception.py", line 34, in inner
    response = get_response(request)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/core/handlers/base.py", line 115, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/core/handlers/base.py", line 113, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/admin/options.py", line 607, in wrapper
    return self.admin_site.admin_view(view)(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/utils/decorators.py", line 130, in _wrapped_view
    response = view_func(request, *args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/views/decorators/cache.py", line 44, in _wrapped_view_func
    response = view_func(request, *args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/admin/sites.py", line 231, in inner
    return view(request, *args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/admin/options.py", line 1638, in add_view
    return self.changeform_view(request, None, form_url, extra_context)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/utils/decorators.py", line 43, in _wrapper
    return bound_method(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/utils/decorators.py", line 130, in _wrapped_view
    response = view_func(request, *args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/admin/options.py", line 1522, in changeform_view
    return self._changeform_view(request, object_id, form_url, extra_context)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/admin/options.py", line 1565, in _changeform_view
self.save_model(request, new_object, form, not add)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/admin/options.py", line 1081, in save_model
    obj.save()
  File "/[...]/django-concurrency-test/apps/main/models/users.py", line 102, in save
    super(DashboardUser, self).save(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/contrib/auth/base_user.py", line 66, in save
    super().save(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 749, in save
    force_update=force_update, update_fields=update_fields)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 787, in save_base
    force_update, using, update_fields,
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 890, in _save_table
    results = self._do_insert(cls._base_manager, using, fields, returning_fields, raw)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/base.py", line 929, in _do_insert
    using=using, raw=raw,
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/manager.py", line 82, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/query.py", line 1204, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/models/sql/compiler.py", line 1394, in execute_sql
    cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/debug_toolbar/panels/sql/tracking.py", line 198, in execute
    return self._record(self.cursor.execute, sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/debug_toolbar/panels/sql/tracking.py", line 133, in _record
    return method(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 100, in execute
    return super().execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 68, in execute
    return self._execute_with_wrappers(sql, params, many=False, executor=self._execute)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 77, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/utils.py", line 86, in _execute
    return self.cursor.execute(sql, params)
  File "/[...]/.virtualenvs/django-concurrency-test/lib/python3.7/site-packages/django/db/backends/sqlite3/base.py", line 396, in execute
    return Database.Cursor.execute(self, query, params)
django.db.utils.OperationalError: database is locked
[25/Oct/2020 11:47:07] "POST /admin/main/dashboarduser/add/ HTTP/1.1" 500 235983
[25/Oct/2020 11:47:07] "POST /admin/main/dashboarduser/add/ HTTP/1.1" 302 0
```
