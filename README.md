# fabric-scripts
This repository is a collection of scripts to automate tasks on remote hosts that otherwise need to be performed by hand through SSH. Such automation is handy when a set of instructions need to be executed on all or a subset of servers in the infrastructure without introducing the overhead of heavy-weight configuration management tools such as [Chef](https://www.chef.io/chef/).

Use cases for such tasks include installing arbitrary software, editing configuration files, starting/stopping services, collecting data and much more - all from multiple servers quickly.

These scripts have been built and tested with Python 3.6 and [Fabric 1.14](http://www.fabfile.org).

## Structure
The repository contains multiple directories, each containing tasks revolving around a specific service or piece of software. For example, the `datadog` directory contains tasks to install the [Datadog](https://datadoghq.com) monitoring agent, configure metrics and logging, restart the agent and so forth.

Directories are completely isolated from each-other and no code is shared amongst them. 

In order to execute a specific task, traverse to the concerned service's directory and run:
```
fab <TASK NAME> --hosts=<HOST 1>,<HOST 2>
fab <TASK NAME> --roles=<ROLE 1>,<ROLE 2>
```

`fab --list` can be used to see all available tasks for the current service.

## Roles
Roles can be used to group servers together based on certain characteristics. For example, all web servers could assume the role `web` and all database servers `db`. Any Fabric task executed over a role would essentially be executed inside all servers assuming that role.

Each directory has a `roles.py` file that is supposed to contain role definitions. More specifically, `roledefs` is a `dict` whose key is the name of a role and its value is a `dict` containing the list of `hosts` and any arbitrary data that needs to be supplied for that role.

For example:
```python
roledefs = {
    "web": {
        "hosts": ["ec2-user@172.168.12.4", "centos@52.46.19.12:22"],
        "nginx_config_file": "/etc/nginx/nginx.conf"
    }
}
```

Note that the role definitions are supposed to be provided by the user.