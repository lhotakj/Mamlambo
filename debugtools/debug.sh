#!/bin/sh +x
if [[ $(id -u) -ne 0 ]] ; then echo "This debug requires to be ran as sudo." ; exit 1 ; fi
PWD=$(pwd)
UPPER="$(dirname "$PWD")"
echo $UPPER
while true; do find $UPPER/ -type f -name "*.py" | entr -c /sbin/apachectl restart; done

