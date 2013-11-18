from cuisine import package_ensure
from cuisine import cd, dir_exists, run, dir_ensure, file_write
from fabric.api import prefix, local, settings, puts
from contextlib import contextmanager

import re

@contextmanager
def virtualenv(path, venv_path='venv'):
    with cd(path), prefix('source %s/bin/activate' % venv_path):
        yield

def virtualenv_ensure(path, system_dependencies='', venv_path='venv', pip_requirements='requirements.txt', 
    not_handled=None):
    package_ensure('python-dev python-pip python-virtualenv')
    package_ensure(system_dependencies)
    with cd(path):
        dir_ensure('downloads')
        if not dir_exists(venv_path):
            run('virtualenv --no-site-packages --distribute %s' % venv_path)
        with virtualenv(path, venv_path):
            run('pip freeze > /tmp/freeze.txt')
            with settings(warn_only=True):
                to_uninstall = run('diff -b -B %s /tmp/freeze.txt | grep ">"' % pip_requirements)
                to_install = run('diff -b -B %s /tmp/freeze.txt | grep "<"' % pip_requirements)
            if to_uninstall:
                to_uninstall = to_uninstall.replace('> ', '')
                to_uninstall = _remove_not_handled(to_uninstall, not_handled)
                if to_uninstall:
                    file_write('/tmp/pip-uninstall.txt', to_uninstall)
                    run('pip uninstall -y -r /tmp/pip-uninstall.txt')
            if to_install:
                to_install = to_install.replace('< ', '')
                file_write('/tmp/pip-install.txt', to_install)
                run('pip install --download-cache downloads -r /tmp/pip-install.txt')

def _remove_not_handled(to_uninstall, not_handled):
    # dont's remove distribute if it's being used'
    to_uninstall = re.sub(r'^distribute.*\n?', '', to_uninstall) 
    puts('Ignoring distribute')
    if not_handled:
        for package in not_handled:
            to_uninstall = re.sub(r'^' + package + '.*\n?', '', to_uninstall) 
            puts('Ignoring %s' % package)

    return to_uninstall