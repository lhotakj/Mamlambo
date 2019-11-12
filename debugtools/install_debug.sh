#/bin/sh +x

if [[ $(id -u) -ne 0 ]] ; then echo "This debug requires to be ran as sudo." ; exit 1 ; fi

if [ -n "$(which yum 2>/dev/null)" ]
then
    sudo yum update
    sudo yum install entr -y 
fi

if [ -n "$(which apt-get 2>/dev/null)" ]
then
    sudo apt-get update
    sudo apt-get install entr -y
fi

