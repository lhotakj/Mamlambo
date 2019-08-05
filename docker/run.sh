#!/bin/bash

# run privileged
docker run --privileged -it --rm -v /sys/fs/cgroup:/sys/fs/cgroup:ro lhotakj/centos-apache-mod_wsgi-python3:3.7.4

# list running dockers 
docker ps

# get ip address
docker inspect <docker_id> | grep "IPAddress"


