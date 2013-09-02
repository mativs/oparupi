from contextlib import contextmanager
from fabric.api import env
from fabric.context_managers import prefix
from cuisine import file_exists, file_update
from cuisine import mode_local, is_local, run
from cuisine import text_template 
from cuisine import package_ensure, package_update
from cuisine import repository_ensure_apt 
from uuid import uuid4


env.venv_script = "source venv/bin/activate"

def local(command, capture=False):
	""" Implementation that handles local mode or run """
	from fabric import api
	return api.local(command, shell="/bin/bash", capture=capture)

def compass():
	""" Script to run compass to watch for changes """
	with prefix(env.venv_script):
		local("python manage.py compass watch")

def runserver():
	""" Script to run the server width django web server """
	with prefix(env.venv_script):
		local("python manage.py runserver")

def setup():
	""" Setup project locally """
	mode_local()
	local("virtualenv --no-site-packages --distribute venv")		
	with prefix(env.venv_script):
		local("pip install -r requirements.txt")
		local("cp oparupi/conf/local.dev.example.py oparupi/conf/local.py")
		file_update('oparupi/conf/local.py', lambda x: text_template(x,{'djangokey':str(uuid4())}))
		local("python manage.py syncdb")
		local("python manage.py migrate")
		local("python manage.py loaddata db/posts.json")
		local("python manage.py loaddata db/tags.json")


def vagrant():
	# change from the default user to 'vagrant'
	env.user = 'vagrant'
	# connect to the port-forwarded ssh
	env.hosts = ['127.0.0.1:2222']
	# use vagrant ssh key
	result = local('vagrant ssh-config | grep IdentityFile', capture=True)
	env.key_filename = result.split()[1]

def deploy():
	repository_ensure_apt('ppa:gunicorn/ppa')
	package_update()
	package_ensure('gunicorn')