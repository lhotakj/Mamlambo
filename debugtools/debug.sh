#!/bin/sh
SET +X
PWD=$(pwd)
UPPER="$(dirname "$PWD")"
echo $UPPER

while true; do find $UPPER/ -type f -name "*.py" | entr -c /sbin/apachectl restart; done

