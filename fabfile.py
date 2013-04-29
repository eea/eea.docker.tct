import os.path

from functools import wraps
from fabric.api import *
from fabric.contrib.files import exists


env['nbsap_target_defs'] = {
    'staging': {
        'host_string': 'edw@whiterussian.edw.ro',
        'nbsap_repo':     '/var/local/nbsap-new',
        'nbsap_sandbox':  '/var/local/nbsap-new/sandbox',
        'nbsap_instance': '/var/local/nbsap-new',
        ###
        'project_root': '/var/local/nbsap-new',
        'virtualenv': 'virtualenv',
        'python': '/var/local/nbsap-new/sandbox/bin/python',
    },
}

env['nbsap_default_target'] = 'staging'

def choose_target(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.pop('target', None)
        if name is None and 'nbsap_target' not in env:
            name = env['nbsap_default_target']

        if name is None:
            target_env = {}
        else:
            target_env = env['nbsap_target_defs'][name]
            target_env['nbsap_target'] = name

        with settings(**target_env):
            return func(*args, **kwargs)

    return wrapper


@task
@choose_target
def install():
    if not exists("%(nbsap_repo)s/.git" % env):
        run("git init '%(nbsap_repo)s'" % env)

    local("git push -f '%(host_string)s:%(nbsap_repo)s' HEAD:incoming" % env)
    with cd(env['nbsap_repo']):
        run("git reset incoming --hard")

    if not exists(env['nbsap_sandbox']):
        run("virtualenv --no-site-packages --distribute '%(nbsap_sandbox)s'" % env)
        run("echo '*' > '%(nbsap_sandbox)s/.gitignore'" % env)

    run("%(nbsap_sandbox)s/bin/pip install -U distribute" % env)

    run("%(nbsap_sandbox)s/bin/pip install "
        "-r %(nbsap_repo)s/requirements.txt"
        % env)

    run("%(nbsap_sandbox)s/bin/pip install -e %(nbsap_repo)s" % env)


def supervisor(root, command):
    run('%s/sandbox/bin/supervisorctl %s' %
        (root, command))


@task
@choose_target
def restart():
    supervisor(env['project_root'], "restart nbsap")


@task
@choose_target
def status():
    supervisor(env['project_root'],"status")


@task
@choose_target
def start():
    supervisor(env['project_root'],"start nbsap")


@task
@choose_target
def stop():
    supervisor(env['project_root'],"stop nbsap")


@task
@choose_target
def drop():
    run("%(nbsap_sandbox)s/bin/python %(nbsap_repo)s/manage.py drop" % env)


@task
@choose_target
def syncdb():
    run("%(nbsap_sandbox)s/bin/python %(nbsap_repo)s/manage.py syncdb" % env)


@task
@choose_target
def build():
    execute('install')
    execute('drop')
    execute('syncdb')


@task
@choose_target
def deploy():
    execute('install')
    execute('stop')
    execute('start')
