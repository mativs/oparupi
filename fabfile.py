from contextlib import contextmanager
from fabric.api import env, cd
from fabric.operations import prompt
from fabric.context_managers import prefix
from cuisine import * 
from cuisine_postgresql import * 
from uuid import uuid4


env.venv_script = "source venv/bin/activate"
env.git_uri = "https://github.com/mativs/oparupi.git"
env.project_name = "oparupi"
env.domain = "oparupi.com"

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
        local("cp oparupi/conf/templates/local.dev.py oparupi/conf/local.py")
        env.djangokey = str(uuid4())
        file_update('oparupi/conf/local.py', lambda x: text_template(x,env))
        local("python manage.py syncdb")
        local("python manage.py migrate")
        local("python manage.py loaddata db/posts.json")
        local("python manage.py loaddata db/tags.json")


def deploy(db_password):
    # repository_ensure_apt('ppa:gunicorn/ppa')
    # package_update()
    # package_ensure('gunicorn')

    # Clean and Update 
    package_clean('git')
    package_update()

    # Database Setup 
    env.db_password = db_password
    env.db_username = 'oparupi_user'
    env.db_name = 'oparupi_db'

    package_ensure('postgresql postgresql-contrib')
    postgresql_role_ensure(env.db_username, env.db_password, createdb=True)
    postgresql_database_ensure(env.db_name, owner=env.db_username,
        locale='en_US.utf8', template='template0', encoding='UTF8')
    
    # Source Deploy
    package_ensure('git')
    if not dir_exists(env.project_path):
        run("git clone %s %s" % (env.git_uri, env.project_path))

    # Source Setup 
    package_ensure('python-dev libpq-dev python-pip python-virtualenv')

    with cd(env.project_path):
        run("virtualenv --no-site-packages --distribute venv")      
        with prefix(env.venv_script):

            # Django Setup
            run("git pull origin master")
            run("pip install -r requirements.txt")
            run("cp oparupi/conf/templates/local.prod.py oparupi/conf/local.py")
            env.djangokey = str(uuid4())
            file_update('oparupi/conf/local.py', lambda x: text_template(x,env))

            # Database Setup
            python_package_ensure('psycopg2')
            run("python manage.py syncdb")
            run("python manage.py migrate")
            run("python manage.py loaddata db/posts.json")
            run("python manage.py loaddata db/tags.json")

            # Web Server Setup
            python_package_ensure('gunicorn setproctitle')
            package_ensure('supervisor')
            run("cp oparupi/conf/templates/gunicorn.conf.py oparupi/conf/gunicorn.py")
            file_update('oparupi/conf/gunicorn.py', lambda x: text_template(x,env))


#### Posible places to deploy ###

def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']
    # vagrant project path
    env.project_path = 'oparupi'
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]
    env.domain = '127.0.0.1:80'

def prod():
    env.project_path = '/var/www/oparupi'

