from contextlib import contextmanager
from fabric.api import env, run
from fabric.context_managers import prefix
from cuisine import file_exists, file_update
from cuisine import mode_local
from cuisine import text_template 
from uuid import uuid4

env.venv_script = "source venv/bin/activate"

"""
Local method that runs with /bin/bash
"""
def local(command):
	from fabric import api
	return api.local(command, shell="/bin/bash") 

def compass():
	with prefix(env.venv_script):
		local("python manage.py compass watch &")

def runserver():
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

def deploy():
	pass