from cuisine import package_ensure, python_package_ensure
from cuisine import run, file_exists, file_read, file_write
from fab.virtualenv import virtualenv
from fab.cuisine_postgresql import postgresql_role_ensure, postgresql_database_ensure
from fab.cuisine_postgresql import run_as_postgres, postgresql_database_check
from fabric.api import env

def postgresql_database_drop(name):
	""" Drop postgresql database by name """
	cmd = 'dropdb -U postgres {name}'.format(name=name)
	run_as_postgres(cmd)

def postgresql_ensure(name, username, path, db_password, config_path='oparupi/conf/local.py'):
    with virtualenv(path):
        package_ensure('postgresql postgresql-contrib')
        python_package_ensure('psycopg2')
    postgresql_role_ensure(username, db_password, createdb=True, update_password=True)
    postgresql_database_ensure(name, owner=username,
        locale='en_US.utf8', template='template0', encoding='UTF8')
