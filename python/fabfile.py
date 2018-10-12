import logging
import roles
from fabric.api import env, task, parallel, sudo, run, local

env.use_ssh_config = True
env.roledefs = roles.roledefs
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


@task(name="install-python27-centos6")
@parallel
def install_python27_centos6():
    logging.info("Subscribing to IUS Yum repository")
    sudo("yum -q -y install https://$(rpm -E '%{?centos:centos}%{!?centos:rhel}%{rhel}').iuscommunity.org/ius-release.rpm")

    logging.info("Installing Python 2.7, Pip & Virtualenv")
    sudo("yum -q -y install python27 python27-devel python27-pip python27-setuptools python27-virtualenv --enablerepo=ius")

    # Uncomment if virtualenv for Python 2.6 isn't installed on the system
    # sudo("ln /usr/bin/virtualenv-2.7 /usr/bin/virtualenv")


@task(name="default", default=True)
def fallback():
    logging.warning("By default, no tasks will be executed. Use \"fab --list\" to get a list of tasks available.")
