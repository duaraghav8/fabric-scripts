# Cloudwatch

## Install cloudwatch logs agent
A set of tasks that help install the Cloudwatch logs agent on a running EC2 instance. These tasks support Amazon Linux 1 & 2 and CentOS 6 & 7.

Note that the task `install-logs-agent-centos-6` assumes that Python 2.7 is already present on the target host running CentOS 6 and is available in `PATH` as `python2.7`. The `python/install-python27-centos6` task in this repository can be used to first install Python 2.7 on the host before running this task.

As described in the Cloudwatch logs agent [installation guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/QuickStartEC2Instance.html), the target EC2 instances must have sufficient IAM permissions to work with the service prior to running any of the tasks.

By default, all tasks assume that the target hosts are in `us-east-1`. This can be changed for all tasks by setting the global variable `aws_region` in the fabfile or per task by supplying the `region` argument to fabric like below:

```bash
fab install-logs-agent-amazonlinux-1:region=ap-southeast-1
```

The default [awslogs.conf](logs-agent-conf/awslogs.conf) must be modified by the user to describe target log files, group and stream names. Note that template strings (strings starting and ending with double underscore) are replaced at runtime depending on the environment the agent is being installed in.