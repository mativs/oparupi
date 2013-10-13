from fab.virtualenv import virtualenv
from cuisine import python_package_ensure, package_ensure
from cuisine import text_template
from cuisine import file_update, dir_ensure
from cuisine import sudo, run, mode_sudo
from fabric.api import env


def gunicorn_ensure(path, template, config):
    with virtualenv(path):
        python_package_ensure('gunicorn')
        run("cp %s %s" % (template, config))
        file_update(config, lambda x: text_template(x,env))
        dir_ensure('%s/logs' % path)
        dir_ensure('%s/run' % path)

def gunicorn_supervisor_ensure(template, config):
    with mode_sudo():
        package_ensure('supervisor')
        python_package_ensure('setproctitle')
        run("cp %s %s" % (template, config))
        file_update(config, lambda x: text_template(x,env))
        run("supervisorctl reread")
        run("supervisorctl update")
        run("supervisorctl restart %s" % (env.project_name))