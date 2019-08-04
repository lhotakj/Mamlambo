#!/bin/bash

RESET='\033[0m'
RED='\033[0;31m'    # Red
GREEN='\033[0;32m'  # Green
YELLOW='\033[0;33m' # Yellow
BOLD='\033[1'

if [ -z "$1" ]; then
  echo "Setting to latest Python version (3.7.4)"
  python_version=3.7.4
else
  echo -e "Setting Python to version ${BOLD}$1${RESET}"
  python_version=$1
fi

install_url=https://www.python.org/ftp/python/
mod_wsgi_source_url=https://github.com/GrahamDumpleton/mod_wsgi/archive
mod_wsgi_source_version=4.6.5

yum install -y -q deltarpm
yum install -y -q make zlib-devel libffi-devel openssl-devel gcc gcc-c++ wget httpd httpd-devel
cd /usr/src
wget --quiet ${install_url}/$python_version/Python-${python_version}.tgz
tar xzf Python-${python_version}.tgz
cd /usr/src/Python-${python_version}
./configure --prefix=/usr/bin/python3.7 --with-ensurepip=yes --enable-silent-rules --disable-tests --enable-shared
export LD_RUN_PATH=/usr/bin/python3.7/lib
CORES=$(nproc --all)
cd /usr/src/Python-${python_version}
make install -j $CORES
rm -f /usr/src/Python-${python_version}.tgz
echo -e "\n# Path to python ${python_version} " >>/etc/bashrc
echo -e "export PATH=\"\$PATH:/usr/bin/python3.7/bin\"" >>/etc/bashrc
ln -sf /usr/bin/python3.7/bin/pip3 /usr/bin/pip3
ln -sf /usr/bin/python3.7/bin/pip3.7 /usr/bin/pip3.7
ln -sf /usr/bin/python3.7/bin/python3.7 /usr/bin/python3.7
ln -sf /usr/bin/python3.7/bin/python3.7m /usr/bin/python3.7m
ln -sf /usr/bin/python3.7/bin/python3.7 /usr/bin/python3
/usr/src/Python-${python_version}/python -m ensurepip
/usr/src/Python-${python_version}/python -m pip install -q --upgrade pip

mkdir -f /tmp/m
cd /tmp/m
wget --quiet ${mod_wsgi_source_url}/${mod_wsgi_source_version}.tar.gz
tar xvfz ./${mod_wsgi_source_version}.tar.gz
cd mod_wsgi-${mod_wsgi_source_version}/
./configure --with-apxs=/bin/apxs --with-python=/usr/bin/python3.7/bin/python3.7
make
make install
cd /
rm -rf /tmp/m

ln -sf /usr/bin/python3.7/lib/libpython3.7m.so.1.0 /lib/libpython3.7m.so.1.0
ln -sf /usr/bin/python3.7/lib/libpython3.7m.so.1.0 /lib64/libpython3.7m.so.1.0

echo -e "# This file loads custom built mod_wsgi $mod_wsgi_source_version with Python $python_version\n\nLoadModule wsgi_module modules/mod_wsgi.so\n\n" >>/etc/httpd/conf.modules.d/10-python-${python_version-wsgi}-${mod_wsgi_source_version}.conf
apachectl restart
echo "Listing moduled"
check=$(apachectl -M 2>/dev/null | grep wsgi_module)
if [ -z "$check" ]; then
  echo -e "${RED}mod_wsgi installation has failed!${RESET}"
else
  echo -e "${GREEN}mod_wsgi sucessfully installed!${RESET}"
fi

server_info=$(curl -s -I -X GET http://localhost | grep "Server:")
echo -e "Server Info: ${YELLOW}${server_info}${RESET}"
