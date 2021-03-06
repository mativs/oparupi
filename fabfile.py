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
env.venv_path = "venv"
env.environment = 'dev'
env.djangokey = str(uuid4())
env.git_uri = "https://github.com/mativs/oparupi.git"
env.git_branch = 'master'
env.db_password = str(uuid4()) 
env.db_username = 'oparupi_db_user'
env.db_name = 'oparupi_database'
env.project_name = "oparupi"
env.project_domain = "oparupi.com"
env.project_path = 'oparupi'
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
    """ Drop and recreate db with remote data and download media files """
    local("rm -f %s" % env.project_sqlite_path)
    django_database_local_setup(env.project_name)
    django_database_pull(env.project_path, env.venv_path)
    django_media_pull(env.project_path,
        env.project_local_media_path, 
        env.project_remote_media_path
    )

@task
def pushdata():
    """ Drop and recreate remote db with local data and upload media files """
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
    git_ensure(env.project_path, env.git_uri, env.git_branch)
    package_ensure(env.project_dependencies)
    virtualenv_ensure(env.project_path, env.venv_path)
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
        env.venv_path
    )
    django_database_ensure(
        env.project_path,
        env.venv_path
    )
    gunicorn_ensure(env.project_path, 
        os.path.join(env.project_path, env.project_gunicorn_template),
        os.path.join(env.project_path, env.project_gunicorn_config),
        env.venv_path
    )
    gunicorn_supervisor_ensure(
        env.project_name,
        os.path.join(env.project_path, env.project_supervisor_template)
    ) 
    nginx_ensure(env.project_name, 
        os.path.join(env.project_path, env.project_nginx_template)
    )
    django_static_ensure(
        env.project_path,
        env.venv_path
    )

def status():
    sudo("supervisorctl status %s" % env.project_name)

@task
def prod():
    """ Set production hosts """
    env.user = 'mativs'
    env.hosts = ['oparupi.com']
    env.project_path = '/home/mativs/oparupi'
    env.environment = 'prod'
    env.project_domain = 'oparupi.com'

