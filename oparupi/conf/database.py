import os
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(SITE_ROOT, 'db.sqlite')
        }
}