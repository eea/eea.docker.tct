from contextlib import contextmanager
from fabric.api import cd, prefix, env, sudo
from glob import glob
from pipes import quote
import ConfigParser
import os


env.colorize_errors = True


def enviroment(location='production'):
    config = ConfigParser.RawConfigParser()
    local_path = os.path.dirname(__file__)
    config.read(os.path.join(local_path, 'env.ini'))
    env.update(config.items(section=location))
    env.project_paths = config.get(location, 'project_root').split(',')


@contextmanager
def virtualenv(directory):
    """
    Context manager to activate an existing Python `virtual environment`_.
        with virtualenv('/path/to/virtualenv'):
            run('python -V')
    """
    # Build absolute path to the virtualenv activation script
    if not os.path.isabs(directory):
        venv_path = os.path.join(env.cwd, directory)
    else:
        venv_path = directory
    activate_path = os.path.join(venv_path, 'bin', 'activate')
    # Source the activation script
    with prefix('. %s' % quote(activate_path)):
        yield


def deploy():
    enviroment()
    for path in env.project_paths:
        with cd(path), virtualenv('env'):
            sudo('git pull --rebase')
            sudo('pip install -r requirements.txt')
            instance_dirs = sudo("ls -1 | grep -E '^instance'")
            for instance in instance_dirs.splitlines():
                sudo('python %s/manage.py syncdb' % instance)
                sudo('python %s/manage.py collectstatic --noinput' % instance)
            sudo('supervisorctl restart all')
