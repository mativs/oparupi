from fabric.api import *
from cuisine import *
from fab.virtualenv import virtualenv_ensure, virtualenv
from fab.gunicorn import gunicorn_ensure, gunicorn_supervisor_ensure, gunicorn_supervisor_restart
from fab.nginx import nginx_ensure
from fab.git import git_ensure
from fab.django import django_config_ensure, django_static_ensure
from fab.django import django_database_ensure, django_database_pull, django_database_push
from fab.django import django_database_local_setup, django_media_pull, django_media_push
from fab.django import django_disable_debug_mode, django_enable_debug_mode
from fab.postgresql import postgresql_ensure
from fab.cuisine_postgresql import postgresql_database_check
from uuid import uuid4
import os
import fab

 # change from the default user to 'vagrant'
env.user = 'mativs'
env.venv_script = "source venv/bin/activate"
env.environment = 'dev'
env.supervisor_config = '/etc/supervisor/conf.d/oparupi.conf'
env.djangokey = str(uuid4())
env.git_uri = "https://github.com/mativs/oparupi.git"
env.git_branch = 'master'
env.db_password = str(uuid4()) 
env.db_username = 'oparupi_db_user'
env.db_name = 'oparupi_database'
env.project_name = "oparupi"
env.project_domain = "oparupi.com"
env.project_path = '.'
env.project_dependencies = 'libjpeg62 libjpeg62-dev zlib1g-dev'
env.project_config_template = 'oparupi/conf/templates/local.%s.py'
env.project_config_path = 'oparupi/conf/local.py'
env.project_gunicorn_template = 'oparupi/conf/templates/gunicorn.conf.py'
env.project_gunicorn_config = 'oparupi/conf/gunicorn.py'
env.project_supervisor_template = 'oparupi/conf/templates/supervisor.conf'
env.project_nginx_template = 'oparupi/conf/templates/nginx.conf'
env.project_sqlite_path = 'oparupi/db.sqlite'
env.project_local_media_path = "media"
env.project_remote_media_path = "media"

@task
def enable_debug():
    """ Enable django debug mode """
    django_enable_debug_mode(env.project_path, env.project_config_path)
    # gunicorn_supervisor_restart(env.project_name)

@task
def disable_debug():
    """ Disable django debug mode """
    django_disable_debug_mode(env.project_path, env.project_config_path)

@task
def pulldata():
    """ Drop and recreate db with remote data and download uploaded files """
    local("rm -f %s" % env.project_sqlite_path)
    django_database_local_setup(env.project_name)
    django_database_pull(env.project_path)
    django_media_pull(env.project_path,
        env.project_local_media_path, 
        env.project_remote_media_path
    )

@task
def pushdata():
    """ Set database to dump state """
    django_database_push(env.project_path,
        env.db_name,
        env.db_username,
        env.db_password,
        env.project_config_template % env.environment,
        env.project_config_path)
    django_media_push(env.project_path,
        env.project_local_media_path,
        env.project_remote_media_path)
    gunicorn_supervisor_restart(env.project_name)

@task
def deploy():
    """ Deploy project to remote location """
    package_clean('git')
    package_update()
    git_ensure(env.project_path, env.git_uri, env.git_branch)
    virtualenv_ensure(env.project_path, env.project_dependencies)
    django_config_ensure(env.project_path,
        env.project_config_template % env.environment,
        env.project_config_path)
    django_disable_debug_mode(
        env.project_path,
        env.project_config_path
    )
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
        env.project_name,
        os.path.join(env.project_path, env.project_supervisor_template),
        env.supervisor_config
    ) 
    nginx_ensure(env.project_name, 
        os.path.join(env.project_path, env.project_nginx_template)
    )
    django_static_ensure(env.project_path)

def status():
    sudo("supervisorctl status %s" % env.project_name)

@task
def vagrant():
    """ Set vagrant as host """
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
    env.key_filename = result.split()[1].strip('"')
    # clean vagrant iso
    
    

@task
def prod():
    """ Set production hosts """
    env.user = 'mativs'
    env.hosts = ['oparupi.com']
    env.project_path = '/home/mativs/oparupi'
    env.environment = 'prod'
    env.project_domain = '*.oparupi.com'

