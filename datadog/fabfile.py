import roles
import time, logging
from fabric.api import env, task, parallel, sudo, run, local

env.use_ssh_config = True
env.roledefs = roles.roledefs
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


@task(name="restart-agent")
@parallel
def restart_agent():
    sudo("restart datadog-agent")
    logging.info("Waiting a few seconds before fetching agent status...")
    time.sleep(4)
    sudo("datadog-agent status")


@task(name="default", default=True)
def fallback():
    logging.warning("By default, no tasks will be executed. Use \"fab --list\" to get a list of tasks available.")
