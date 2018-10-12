# Python

### Install Python 2.7 on CentOS 6
As [this post](https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4) explains, CentOS 6 comes shipped with Python 2.6, whereas most python-based apps and tools require 2.7+. Unfortunately, it isn't straightforward to work with Python 2.7 on CentOS 6, since removing 2.6 from the system is not an option. These versions must therefore co-exist with Python 2.6 remaining in `PATH` as the default python.

This task cleanly installs Python 2.7, pip, virtualenv and other necessary tools on CentOS 6.