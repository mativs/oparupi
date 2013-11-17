from fab.virtualenv import virtualenv
from cuisine import file_update, text_template
from cuisine import cd, run
from fabric.api import get, put, local, env, lcd

from fab.postgresql import postgresql_database_check, postgresql_database_drop, postgresql_ensure


import re
import os

def django_enable_debug_mode(project_path, config):
    with cd(project_path):
        file_update(config, lambda x: re.sub('DEBUG = \w*', 'DEBUG = True', x) )

def django_disable_debug_mode(project_path, config):
    with cd(project_path):
        file_update(config, lambda x: re.sub('DEBUG = \w*', 'DEBUG = False', x) )

def django_config_ensure(path, template, config):
    with cd(path):
        run("cp %s %s" % (template, config))
        file_update(config, lambda x: text_template(x,env))

def django_static_ensure(path, venv_path='venv'):
    with virtualenv(path, venv_path):
        run("python manage.py collectstatic --noinput")

def django_database_ensure(path, venv_path='venv', migration=''):
	with virtualenv(path):
		run("python manage.py syncdb --noinput")
		run("python manage.py migrate %s" % migration)

def django_database_pull(project_path):
    """ Dump remote database and load it locally """
    with virtualenv(project_path):
        run("python manage.py dumpdata > /tmp/db.json")
        get('/tmp/db.json', '/tmp/db.json')
    local("python manage.py loaddata /tmp/db.json")

def django_database_push(project_path, db_name, db_username, db_password, config_template_path, config_path):
    """ Recreate and load local database to remote host"""
    local("python manage.py dumpdata > /tmp/db.json")
    with cd(project_path):
        put('/tmp/db.json', '/tmp/db.json')
    if postgresql_database_check(db_name):
        postgresql_database_drop(db_name)
    django_config_ensure(project_path,
        config_template_path,
        config_path)
    postgresql_ensure(db_name, db_username, project_path, db_password )
    django_database_ensure(project_path )    
    with virtualenv(project_path):
        run("python manage.py loaddata /tmp/db.json")

def django_database_local_setup(project_name):
    """ Setup local django database """
    local("python manage.py syncdb --noinput")
    local("python manage.py migrate")

def django_media_pull(project_path, local_media_path, remote_media_path):
    """ Overwrite local media files with remote ones """
    with cd(project_path), cd(remote_media_path):
        run('tar -czf /tmp/media.tar.gz *')
        get('/tmp/media.tar.gz', '/tmp/media.tar.gz')
    local("mkdir -p %s" % (local_media_path)) 
    local("rm -rf %s/*" % (local_media_path))
    local("tar -xf /tmp/media.tar.gz -C %s" % (local_media_path)) 

def django_media_push(project_path, local_media_path, remote_media_path):
    with lcd(local_media_path):
        local('tar -czf /tmp/media.tar.gz *')
    put('/tmp/media.tar.gz', '/tmp/media.tar.gz')
    
    with cd(project_path):
        run("mkdir -p %s" % (remote_media_path)) 
        with cd(remote_media_path):
            run("rm -rf *")
            run("tar -xf /tmp/media.tar.gz") 

