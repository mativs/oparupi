from cuisine import package_ensure
from cuisine import file_update, file_exists
from cuisine import text_template
from cuisine import mode_sudo, run
from fabric.api import env

def nginx_ensure(name, template):
	with mode_sudo():
	    package_ensure('nginx') 
	    run("cp %s /etc/nginx/sites-available/%s" % (template, name))
	    file_update('/etc/nginx/sites-available/%s' % name, lambda x: text_template(x,env))
	    if not file_exists("/etc/nginx/sites-enabled/%s" % name):
	        run("ln -s -t /etc/nginx/sites-enabled /etc/nginx/sites-available/%s " % (
	            env.project_name))
	    run("service nginx restart")