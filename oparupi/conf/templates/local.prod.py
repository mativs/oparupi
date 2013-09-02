import os
from oparupi.conf.default import *

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_username}',
        'PASSWORD': '${db_password}',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}

SECRET_KEY = '${djangokey}'
