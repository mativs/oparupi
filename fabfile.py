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
env.project_path = '/home/mativs/oparupi'

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

def setup_database(db_password):
    """ Setup Database on host """
    env.db_password = db_password
    env.db_username = 'oparupi_user'
    env.db_name = 'oparupi_db'

    package_ensure('postgresql postgresql-contrib')
    postgresql_role_ensure(env.db_username, env.db_password, createdb=True)
    postgresql_database_ensure(env.db_name, owner=env.db_username,
        locale='en_US.utf8', template='template0', encoding='UTF8')

def source_deploy():
    """ Deploy project source on host """
    package_ensure('git')
    if not dir_exists(env.project_path):
        run("git clone %s %s" % (env.git_uri, env.project_path))

def source_update():
    package_ensure('python-dev libpq-dev python-pip python-virtualenv')
    with cd(env.project_path):
        run("git pull origin master")

def virtualenv_setup():
    with cd(env.project_path):
        run("virtualenv --no-site-packages --distribute venv") 

def django_setup():
    with cd(env.project_path), prefix(env.venv_script):
        # Django Setup
        run("git pull origin master")
        run("pip install -r requirements.txt")
        run("cp oparupi/conf/templates/local.prod.py oparupi/conf/local.py")
        env.djangokey = str(uuid4())
        file_update('oparupi/conf/local.py', lambda x: text_template(x,env))

def database_setup():
    with cd(env.project_path), prefix(env.venv_script):
        python_package_ensure('psycopg2')
        run("python manage.py syncdb")
        run("python manage.py migrate")
        # run("python manage.py loaddata db/posts.json")
        # run("python manage.py loaddata db/tags.json")

def gunicorn_setup():
    with cd(env.project_path), prefix(env.venv_script):
        python_package_ensure('gunicorn setproctitle')
        package_ensure('supervisor')
        run("cp oparupi/conf/templates/gunicorn.conf.py oparupi/conf/gunicorn.py")
        file_update('oparupi/conf/gunicorn.py', lambda x: text_template(x,env))
        mode_sudo()
        with mode_sudo():
            sudo("cp oparupi/conf/templates/supervisor.conf /etc/supervisor/conf.d/oparupi.conf")
            file_update('/etc/supervisor/conf.d/oparupi.conf', lambda x: text_template(x,env))
            sudo("supervisorctl reread")
            sudo("supervisorctl update")

def status():
    sudo("supervisorctl status %s" % env.project_name)

def host_clean():
    package_clean('git')
    package_update()

def deploy(db_password):
    host_clean()
    host_update()
    setup_database(db_password)
    source_deploy()
    virtualenv_setup()
    django_setup()
    gunicorn_setup()    
    
    

           
#### Posible places to deploy ###

def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']
    # vagrant project path
    env.project_path = '/home/vagrant/oparupi'
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]
    env.domain = '0.0.0.0:80'

def prod():
    env.project_path = '/var/www/oparupi'

