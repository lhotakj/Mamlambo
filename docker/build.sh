#!/bin/bash
sudo docker pull centos:7

python_versions=(3.4.0 3.5.0 3.6.0 3.7.3 3.7.4)
python_versions_count=${#python_versions[@]}
loop=0

for python_version in "${python_versions[@]}"
do
    sudo docker build . -t centos-apache-mod_wsgi-python3:${python_version} --force-rm --build-arg python_version=${python_version}
    sudo docker tag centos-apache-mod_wsgi-python3:${python_version} lhotakj/centos-apache-mod_wsgi-python3:${python_version}
    sudo docker push lhotakj/centos-apache-mod_wsgi-python3:${python_version}
    loop=$((loop + 1))
    if [ "$loop" -eq "$python_versions_count" ];then
        sudo docker tag centos-apache-mod_wsgi-python3:${python_version} lhotakj/centos-apache-mod_wsgi-python3:latest
        sudo docker push lhotakj/centos-apache-mod_wsgi-python3:latest
    fi
done

sudo docker image ls

