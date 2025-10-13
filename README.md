# My Django Project with MySQL
This is a Django project connected to MySQL database.

## Setup steps
1. Create a MySQL database
2. Update settings.py with DB credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
