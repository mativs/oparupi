from fabric.api import env
from cuisine import mode_local
from cuisine import run
from cuisine import package_clean, package_update
from fab import local
from fab.git import git_ensure
from fab.virtualenv import virtualenv_ensure, virtualenv
from fab.gunicorn import gunicorn_ensure, gunicorn_supervisor_ensure
from fab.nginx import nginx_ensure
from fab.django import django_config_ensure, django_static_ensure, django_database_ensure
from fab.postgresql import postgresql_ensure
from uuid import uuid4
import os

env.venv_script = "source venv/bin/activate"
env.git_uri = "https://github.com/mativs/oparupi.git"
env.git_branch = 'master'
env.project_name = "oparupi"
env.project_domain = "oparupi.com"
env.project_path = '/home/mativs/oparupi'
env.project_dependencies = 'libpq-dev'
env.project_config_template = 'oparupi/conf/templates/local.%s.py'
env.project_config_path = 'oparupi/conf/local.py'
env.project_gunicorn_template = 'oparupi/conf/templates/gunicorn.conf.py'
env.project_gunicorn_config = 'oparupi/conf/gunicorn.py'
env.project_supervisor_template = 'oparupi/conf/templates/supervisor.conf'
env.project_nginx_template = 'oparupi/conf/templates/nginx.conf'
env.system_dependencies = 'libpq-dev'
env.supervisor_config = '/etc/supervisor/conf.d/oparupi.conf'
env.djangokey = str(uuid4())
env.db_password = str(uuid4())
env.db_username = 'oparupi_user'
env.db_name = 'oparupi_db'

def compass():
    with prefix(env.venv_script):
        local("python manage.py compass watch")

def runserver():
    """ Script to run the server width django web server """
    with prefix(env.venv_script):
        local("python manage.py runserver")

def database_setup():
    with virtualenv(env.project_path):
        run("python manage.py syncdb --noinput")
        run("python manage.py migrate")

def database_restore(db_dump_path):
    """ Set database to dump state """
    if is_remote():
        if postgresql_database_check(env.db_name):
            postgresql_database_drop(env.db_name)
        postgresql_ensure(env.project_path)
    database_setup()
    put(db_dump_path, "%s/db/db.json" % env.project_path )
    with cd(env.project_path), prefix(env.venv_script):
        run("python manage.py loaddata db/db.json")

def project_ensure():
    git_ensure(env.project_path, env.git_uri, env.git_branch)
    virtualenv_ensure(env.project_path, env.system_dependencies)
    django_config_ensure(env.project_path,
        env.project_config_template % env.environment,
        env.project_config_path)

def web_server_ensure():
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

def database_ensure():
    postgresql_ensure(
        env.db_name,
        env.db_username,
        env.db_password,
        env.project_path
    )
    django_database_ensure(env.project_path)

def static_ensure():
    django_static_ensure(env.project_path)

def status():
    sudo("supervisorctl status %s" % env.project_name)

def host_clean():
    """ Clean old git in ubuntu 12.04 """
    package_clean('git')
    package_update()
    
def setup():
    host_clean()
    project_ensure()
    web_server_ensure()
    database_ensure()
    static_ensure()

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
    env.domain = '0.0.0.0:80'
    # set database dependencies
    env.database_dependencies = 'postgresql postgresql-contrib'
    # start vagrant
    local("vagrant up")
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]
    # clean vagrant iso

def dev():
    env.project_path = '.'
    env.environment = 'dev'
    env.domain = 'localhost'
    env.database_dependencies = ''
    mode_local()
