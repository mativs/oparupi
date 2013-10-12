from fab.virtualenv import virtualenv
from cuisine import file_update, text_template
from cuisine import cd, run,file_write, file_exists, file_read
from fabric.api import env
from uuid import uuid4

import re

PASSWORD_PATTERN = "\'PASSWORD\'\:[ ]*\'(.*)\'"

def django_dbpassword_get(path, config):
    with cd(path):
    	password = str(uuid4())
    	if file_exists(config):
    		matches = re.findall(PASSWORD_PATTERN, file_read(config))
    		if len(matches) > 0 and len(matches[0].strip()) > 0:
    			password = matches[0]
    	return password

def django_config_ensure(path, template, config, db_password_path='db_password'):
    with cd(path):
        run("cp %s %s" % (template, config))
        file_update('%s' % config, lambda x: text_template(x,env))
        file_write(db_password_path, env.db_password)

def django_static_ensure(path, venv_path='venv'):
    with virtualenv(path, venv_path):
        run("python manage.py collectstatic --noinput")

def django_database_ensure(path, venv_path='venv', migration=''):
	with virtualenv(path):
		run("python manage.py syncdb --noinput")
		run("python manage.py migrate %s" % migration)
