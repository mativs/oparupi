from fabric.api import env, put, cd
from fab.cuisine_postgresql import postgresql_database_check
from fab.postgresql import postgresql_database_drop
from cuisine import mode_local, is_remote
from cuisine import run
from cuisine import package_clean, package_update
from cuisine import dir_ensure
from fab import local
from fab.git import git_ensure
from fab.virtualenv import virtualenv_ensure, virtualenv
from fab.gunicorn import gunicorn_ensure, gunicorn_supervisor_ensure
from fab.nginx import nginx_ensure
from fab.django import django_config_ensure, django_static_ensure, django_database_ensure
from fab.postgresql import postgresql_ensure
from uuid import uuid4
import os

 # change from the default user to 'vagrant'
env.venv_script = "source venv/bin/activate"
env.environment = 'dev'
env.system_dependencies = 'libpq-dev'
env.supervisor_config = '/etc/supervisor/conf.d/oparupi.conf'
env.djangokey = str(uuid4())
env.git_uri = "https://github.com/mativs/oparupi.git"
env.git_branch = 'master'
env.db_password = str(uuid4()) 
env.db_username = 'oparupi_db_user'
env.db_name = 'oparupi_db_name'
env.project_name = "oparupi"
env.project_domain = "oparupi.com"
env.project_path = '.'
env.project_dependencies = 'libpq-dev'
env.project_config_template = 'oparupi/conf/templates/local.%s.py'
env.project_config_path = 'oparupi/conf/local.py'
env.project_gunicorn_template = 'oparupi/conf/templates/gunicorn.conf.py'
env.project_gunicorn_config = 'oparupi/conf/gunicorn.py'
env.project_supervisor_template = 'oparupi/conf/templates/supervisor.conf'
env.project_nginx_template = 'oparupi/conf/templates/nginx.conf'
env.project_sqlite_path = 'oparupi/db.sqlite'
env.project_dump_path = "db/"

def compass():
    with prefix(env.venv_script):
        local("python manage.py compass watch")

def runserver():
    """ Script to run the server width django web server """
    with prefix(env.venv_script):
        local("python manage.py runserver")

def restore(db_dump_path):
    """ Set database to dump state """
    with cd(env.project_path):
        dir_ensure(env.project_dump_path)
        put(db_dump_path, env.project_dump_path)
    if postgresql_database_check(env.db_name):
        postgresql_database_drop(env.db_name)
    postgresql_ensure(
        env.db_name,
        env.db_username,
        env.project_path,
        env.db_password
    )   
    django_database_ensure(env.project_path )
    with virtualenv(env.project_path):
        run("python manage.py loaddata db/db.json")

def status():
    sudo("supervisorctl status %s" % env.project_name)

def deploy():
    

    git_ensure(env.project_path, env.git_uri, env.git_branch)
    virtualenv_ensure(env.project_path, env.system_dependencies)
    django_config_ensure(env.project_path,
        env.project_config_template % env.environment,
        env.project_config_path)
    postgresql_ensure(
        env.db_name,
        env.db_username,
        env.project_path,
        env.db_password,
        update_password=True
    )
    django_database_ensure(env.project_path)
    gunicorn_ensure(env.project_path, 
        os.path.join(env.project_path, env.project_gunicorn_template),
        os.path.join(env.project_path, env.project_gunicorn_config)
    )
    gunicorn_supervisor_ensure(
        os.path.join(env.project_path, env.project_supervisor_template),
        env.supervisor_config
    ) 
    nginx_ensure(env.project_name, 
        os.path.join(env.project_path, env.project_nginx_template)
    )
    django_static_ensure(env.project_path)


##_gunicorn_templateo deploy ###
def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']
    # vagrant project path
    env.project_path = '/home/vagrant/oparupi'
    # environment
    env.environment = 'prod'
    # set local domain
    env.project_domain = '0.0.0.0:80'
    # start vagrant
    local("vagrant up")
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]
    # clean vagrant iso
    """ Clean old git in ubuntu 12.04 """
    package_clean('git')
    package_update()

def prod():
    env.user = 'root'
    env.hosts = ['oparupi.com']
    env.project_path = '/root/oparupi'
    env.environment = 'prod'
    env.project_domain = '*.oparupi.com'