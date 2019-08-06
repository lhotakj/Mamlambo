#!/bin/bash

# run apache on port 89
sudo docker run -idt --rm -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 89:80 --tmpfs /run --tmpfs /run/lock --name=apache lhotakj/centos-apache-mod_wsgi-python3:3.7.4

sudo docker cp ./demo apache:/tmp ...

# enter container
sudo docker exec -it  apache /bin/bash

# kill at the end
sudo docker container kill apache



# list running dockers 
docker ps

# get ip address
docker inspect <docker_id> | grep "IPAddress"


