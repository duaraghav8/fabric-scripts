import roles
import time, logging
from fabric.api import env, task, parallel, sudo, run, local

env.use_ssh_config = True
env.roledefs = roles.roledefs
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


# Global configuration
aws_region = "us-east-1"


def install_logs_agent_amazonlinux(region):
    state_file = "/var/lib/awslogs/agent-state"

    logging.info("Updating and installing awslogs package")
    sudo("yum update -y -q")
    sudo("yum install -y -q awslogs")

    logging.info("Configuring host region")
    sudo("sed -i 's/us-east-1/{}/' /etc/awslogs/awscli.conf".format(region))

    with open("./logs-agent-conf/awslogs.conf", "r") as conf_file:
        awslogs_conf = conf_file \
            .read() \
            .replace("__STATE_FILE__", state_file)

        logging.info("Writing to /etc/awslogs/awslogs.conf")
        sudo("echo \"{}\" > /etc/awslogs/awslogs.conf".format(awslogs_conf))


def install_logs_agent_centos(region):
    setup_script = "https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py"
    state_file = "/var/awslogs/state/agent-state"

    with open("./logs-agent-conf/awslogs.conf", "r") as conf_file:
        awslogs_conf = conf_file \
            .read() \
            .replace("__STATE_FILE__", state_file)

        logging.info("Writing to /tmp/awslogs.conf")
        sudo("echo \"{}\" > /tmp/awslogs.conf".format(awslogs_conf))

    logging.info("Installing Logs agent via setup script")
    sudo("curl {} -o /tmp/awslogs-agent-setup.py".format(setup_script))
    sudo("python2.7 /tmp/awslogs-agent-setup.py -n --region {} -c /tmp/awslogs.conf".format(region))

    logging.info("Cleaning up")
    sudo("rm -f /tmp/{awslogs.conf,awslogs-agent-setup.py}")


@task(name="install-logs-agent-amazonlinux-1")
@parallel
def install_logs_agent_amazonlinux_1(region=aws_region):
    install_logs_agent_amazonlinux(region)

    logging.info("Starting cloudwatch logs agent service")
    sudo("chkconfig awslogs on")
    sudo("service awslogs start")


@task(name="install-logs-agent-amazonlinux-2")
@parallel
def install_logs_agent_amazonlinux_2(region=aws_region):
    install_logs_agent_amazonlinux(region)

    logging.info("Starting cloudwatch logs agent service")
    sudo("systemctl enable awslogsd.service")
    sudo("systemctl start awslogsd")


@task(name="install-logs-agent-centos-6")
@parallel
def install_logs_agent_centos_6(region=aws_region):
    install_logs_agent_centos(region)
    logging.info("Starting awslogs")
    sudo("service awslogs start")


@task(name="install-logs-agent-centos-7")
@parallel
def install_logs_agent_centos_7(region=aws_region):
    install_logs_agent_centos(region)
    logging.info("Starting awslogs")
    sudo("systemctl start awslogs")


@task(name="default", default=True)
def fallback():
    logging.warning("By default, no tasks will be executed. Use \"fab --list\" to get a list of tasks available.")
