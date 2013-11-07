from cuisine import package_ensure, dir_exists
from cuisine import cd, run

def git_is_origin(path, uri):
    with cd(path):
        return run('git config --get remote.origin.url').endswith(uri)

def git_ensure(path, uri, branch):
    package_ensure('git')
    if dir_exists(path) and not git_is_origin(path, uri):
        run("rm -rf %s" % path)
    if not dir_exists(path):
        run("git clone %s %s" % (uri, path))
    with cd(path):
        run('git checkout .')
        run('git checkout %s' % branch)
        run('git pull origin %s' % branch)        

