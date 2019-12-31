# django-simple-admin-email

## Requirements
- Python (>=3.6)
- Django (>= 2.2.4)
- django-crispy-forms (>=1.7.2)

# Installation

Install using
```
pip: 
```
```
pip install django-simple-admin-email
```

Make sure to add the app and crispy_forms to your settings.
```
INSTALLED_APPS = (
    ...
    'crispy_forms',
    'django_simple_admin_email'
    ...
)

```

Make sure that basic email settings are configured. 
Here is an example of what it might look like for a Gmail account, but more likely than not, you won't be using Gmail.

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'simpleadminemail@gmail.com'
EMAIL_HOST_PASSWORD = 'Verygoodpassword1'
```
## Changelog

## Todo