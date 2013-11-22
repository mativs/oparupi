from cuisine import package_ensure, python_package_ensure
from cuisine import run, file_exists, file_read, file_write
from fab.virtualenv import virtualenv
from fab.cuisine_postgresql import postgresql_role_ensure, postgresql_database_ensure
from fab.cuisine_postgresql import run_as_postgres, postgresql_database_check
from fabric.api import env
from fabric.context_managers import cd, hide, settings
from fabric.operations import sudo

def postgresql_database_drop(name):
	""" Drop postgresql database by name """
	cmd = 'dropdb -U postgres {name}'.format(name=name)
	run_as_postgres(cmd)

def postgresql_ensure(name, username, path, db_password, venv_path='.venv'):
    with virtualenv(path, venv_path):
        package_ensure('postgresql postgresql-contrib libpq-dev')
        python_package_ensure('psycopg2')
    postgresql_role_ensure(username, db_password, createdb=True)
    postgresql_database_ensure(name, owner=username,
        locale='en_US.utf8', template='template0', encoding='UTF8')

def psotgresql_table_check(table_name, database_name):
    cmd = 'psql -tAc "SELECT 1 FROM pg_tables WHERE tablename = \'{table_name}\'" -d {database_name}'
    with settings(hide('everything'), warn_only=True):
        return run_as_postgres(cmd.format(table_name=table_name, database_name=database_name)) == '1'

def run_as_postgres(cmd):
    """
    Run given command as postgres user.
    """
    # The cd below is needed to avoid the following warning:
    #
    #     could not change directory to "/root"
    #
    with cd('/'):
        return sudo(cmd, user='postgres')