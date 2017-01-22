=========
MailAdmin
=========

MailAdmin is a web-based email administration software. You can manage domains, accounts, lists and much more.

Quick start
-----------

1. Add "mailadmin" to your INSTALLED_APPS settings like this::
    INSTALLED_APPS = [
        ...
        'mailadmin',
    ]

2. Include the mailadmins URLconf in your project urls.py like this::
    url(r'^mailadmin/', include('mailadmin.urls'))

3. Run `python manage.py migrate` to create the necessary models.

4. Run `python manage.py createadmin` to create an admin user to start with

5. Run `python manage.py runserver` to start the development server

6. Visit http://localhost:8000/mailadmin/ and login with user created admin user
