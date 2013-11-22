from cuisine import package_ensure
from cuisine import cd, dir_exists, run, dir_ensure
from fabric.api import prefix, settings, puts
from contextlib import contextmanager

@contextmanager
def virtualenv(path, venv_path='.venv'):
    with cd(path), prefix('source %s/bin/activate' % venv_path):
        yield

def virtualenv_ensure(project_path, venv_path='.venv', packages_file='requirements.txt', restart=False):
    package_ensure('python-dev python-pip python-virtualenv')
    with virtualenv(project_path, venv_path):
        dir_ensure('downloads')
        if restart:
            run('rm -rf %s' % venv_path)
        if not dir_exists(venv_path):
            run('virtualenv --no-site-packages --distribute %s' % venv_path)
        run('pip install --download-cache downloads -r ' + packages_file)