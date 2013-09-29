from cuisine import package_ensure, python_package_install_pip
from cuisine import cd, dir_exists, run
from fabric.api import prefix
from contextlib import contextmanager

@contextmanager
def virtualenv(path, venv_path='venv'):
    with cd(path), prefix('source %s/bin/activate' % venv_path):
        yield

def virtualenv_ensure(path, system_dependencies='', venv_path='venv', pip_requirements='requirements.txt'):
    package_ensure('python-dev python-pip python-virtualenv')
    package_ensure(system_dependencies)
    with cd(path):
        if dir_exists(venv_path):
            run('rm -rf %s' % venv_path)
        run('virtualenv --no-site-packages --distribute %s' % venv_path)
        with virtualenv(path, venv_path):
        	run('pip install -r %s' % pip_requirements)

