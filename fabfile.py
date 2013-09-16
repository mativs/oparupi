from contextlib import contextmanager
from fabric.api import env, cd, put
from fabric.utils import puts
from fabric.operations import prompt
from fabric.context_managers import prefix
from cuisine import * 
from cuisine_postgresql import * 
from cuisine_postgresql import run_as_postgres
from uuid import uuid4


env.venv_script = "source venv/bin/activate"
env.git_uri = "https://github.com/mativs/oparupi.git"
env.project_name = "oparupi"
env.project_domain = "oparupi.com"
env.project_path = '/home/mativs/oparupi'
env.djangokey = str(uuid4())
env.db_username = 'oparupi_user'
env.db_name = 'oparupi_db'

##### Help methods ####

def local(command, capture=False):
    """ Implementation that handles local mode or run """
    from fabric import api
    return api.local(command, shell="/bin/bash", capture=capture)

def postgresql_database_drop(database_name):
    cmd = 'dropdb -U postgres {database_name}'.format(
        database_name=database_name,
    )
    run_as_postgres(cmd)

# def compass():
#     """ Script to run compass to watch for changes """
#     with prefix(env.venv_script):
#         local("python manage.py compass watch")

# def runserver():
#     """ Script to run the server width django web server """
#     with prefix(env.venv_script):
#         local("python manage.py runserver")

# def setup():
#     """ Setup project locally """
#     mode_local()
#     local("virtualenv --no-site-packages --distribute venv")        
#     with prefix(env.venv_script):
#         local("pip install -r requirements.txt")
#         local("cp oparupi/conf/templates/local.dev.py oparupi/conf/local.py")
#         env.djangokey = str(uuid4())
#         file_update('oparupi/conf/local.py', lambda x: text_template(x,env))
#         local("python manage.py syncdb")
#         local("python manage.py migrate")
#         local("python manage.py loaddata db/posts.json")
#         local("python manage.py loaddata db/tags.json")

def database_create():
    postgresql_database_ensure(env.db_name, owner=env.db_username,
        locale='en_US.utf8', template='template0', encoding='UTF8')

def database_setup(db_password):
    """ Setup Database on host """
    env.db_password = db_password
    package_ensure('postgresql postgresql-contrib')
    postgresql_role_ensure(env.db_username, env.db_password, createdb=True)
    database_create()

def django_database_setup():
    with cd(env.project_path), prefix(env.venv_script):
        python_package_ensure('psycopg2')
        run("python manage.py syncdb --noinput")
        run("python manage.py migrate")
        run("python manage.py createcachetable %s_cache" % (env.project_name))

def python_setup():
    package_ensure('python-dev libpq-dev python-pip python-virtualenv')

def source_deploy():
    """ Deploy project source on host """
    package_ensure('git')
    if not dir_exists(env.project_path):
        run("git clone %s %s" % (env.git_uri, env.project_path))

def source_update():
    package_ensure('git')
    with cd(env.project_path):
        run("git pull origin master")

def virtualenv_setup():
    with cd(env.project_path):
        run("virtualenv --no-site-packages --distribute venv") 

def django_update(db_password):
    env.db_password = db_password
    with cd(env.project_path), prefix(env.venv_script):
        run("git pull origin master")
        run("pip install -r requirements.txt")
        run("cp oparupi/conf/templates/local.prod.py oparupi/conf/local.py")
        file_update('oparupi/conf/local.py', lambda x: text_template(x,env))
        run("python manage.py collectstatic --noinput")
        run("python manage.py syncdb --noinput")
        run("python manage.py migrate")

def gunicorn_setup():
    with cd(env.project_path), prefix(env.venv_script):
        python_package_ensure('gunicorn setproctitle')
        package_ensure('supervisor')
        run("cp oparupi/conf/templates/gunicorn.conf.py oparupi/conf/gunicorn.py")
        file_update('oparupi/conf/gunicorn.py', lambda x: text_template(x,env))
        dir_ensure('%s/logs' % env.project_path)
        dir_ensure('%s/run' % env.project_path)
        with mode_sudo():
            sudo("cp oparupi/conf/templates/supervisor.conf /etc/supervisor/conf.d/oparupi.conf")
            file_update('/etc/supervisor/conf.d/oparupi.conf', lambda x: text_template(x,env))
            sudo("supervisorctl reread")
            sudo("supervisorctl update")

def nginx_setup():
    with cd(env.project_path), prefix(env.venv_script), mode_sudo():
        package_ensure('nginx') 
        sudo("cp oparupi/conf/templates/nginx.conf /etc/nginx/sites-available/%s", env.project_name)
        file_update('/etc/nginx/sites-available/%s' % env.project_name, lambda x: text_template(x,env))
        if not file_exists("/etc/nginx/sites-enabled/%s" % env.project_name):
            sudo("ln -s -t /etc/nginx/sites-enabled /etc/nginx/sites-available/%s %s" % (
                env.project_name, env.project_name))
        sudo("service nginx restart")

def restore_database(db_dump_path):
    put(db_dump_path, "%s/db/db.json" % env.project_path )
    if postgresql_database_check(env.db_name):
        postgresql_database_drop(env.db_name)
    database_create()
    django_database_setup()
    with cd(env.project_path), prefix(env.venv_script):
        run("python manage.py loaddata db/db.json")


def status():
    sudo("supervisorctl status %s" % env.project_name)

def host_clean():
    package_clean('git')
    package_update()

def deploy(db_password):
    host_clean()
    database_setup(db_password)
    python_setup()
    source_deploy()
    virtualenv_setup()
    django_update(db_password)
    django_database_setup()
    gunicorn_setup()   
    nginx_setup()

def update(db_password):
    source_update()
    django_update(db_password)

           
#### Posible places to deploy ###

def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']
    # vagrant project path
    env.project_path = '/home/vagrant/oparupi'
    # start vagrant
    local("vagrant up")
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]
    # set local domain
    env.domain = '0.0.0.0:80'

def prod():
    env.project_path = '/var/www/oparupi'

