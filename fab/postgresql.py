from cuisine_postgresql import postgresql_role_ensure, postgresql_database_ensure
from cuisine_postgresql import run_as_postgres
from cuisine import package_ensure, python_package_ensure
from cuisine import run
from fab.virtualenv import virtualenv

def postgresql_database_drop(name):
	""" Drop postgresql database by name """
	cmd = 'dropdb -U postgres {name}'.format(name=name)
	run_as_postgres(cmd)

def postgresql_ensure(name, username, password, path):
    package_ensure('postgresql postgresql-contrib')
    postgresql_role_ensure(username, password, createdb=True)
    postgresql_database_ensure(name, owner=username,
            locale='en_US.utf8', template='template0', encoding='UTF8')
    with virtualenv(path):
        python_package_ensure('psycopg2')