#!/bin/bash

# het the latest centos image
sudo docker pull centos:7

# set constants
docker_hub_user=lhotakj
docker_hub_repo=centos-apache-mod_wsgi-python3
python_versions=(3.4.0 3.5.0 3.6.0 3.7.0 3.7.1 3.7.2 3.7.3 3.7.4)
python_versions_count=${#python_versions[@]}

loop=0
for python_version in "${python_versions[@]}"
do
    sudo docker build . -t ${docker_hub_repo}:${python_version} --force-rm --build-arg python_version=${python_version}
    sudo docker tag ${docker_hub_repo}:${python_version} ${docker_hub_user}/${docker_hub_repo}:${python_version}
    sudo docker push ${docker_hub_user}/${docker_hub_repo}:${python_version}
    loop=$((loop + 1))
    if [ "$loop" -eq "$python_versions_count" ];then
        sudo docker tag ${docker_hub_repo}:${python_version} ${docker_hub_user}/${docker_hub_repo}:latest
        sudo docker push ${docker_hub_user}/${docker_hub_repo}:latest
    fi
done

sudo docker image ls

