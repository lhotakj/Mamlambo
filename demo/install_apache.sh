PORT=99
USER=jarda

# http://www.eatdirtshit.rocks/how-i-got-python-3-6-1-and-wsgi-working-on-centos-7-3/
# https://stackoverflow.com/questions/42004986/how-to-install-mod-wgsi-for-apache-2-4-with-python3-5-on-centos-7
# https://stackoverflow.com/questions/30642894/getting-flask-to-use-python3-apache-mod-wsgi
# https://developers.redhat.com/blog/2018/08/13/install-python3-rhel/
# https://modwsgi.readthedocs.io/en/develop/user-guides/checking-your-installation.html#python-shared-library
# https://django.readthedocs.io/en/2.2.x/howto/deployment/wsgi/modwsgi.html

# maybe https://groups.google.com/forum/#!topic/modwsgi/Dh_CkhRKwGw

# list all
# yum search mod_wsgi

sudo yum install centos-release-scl

# in case mod_wsgi (python 2.7) installed, remove it
sudo yum remove mod_wsgi -y -q
sudo yum install -y -q rh-python36-mod_wsgi.x86_64
scl enable rh-python36 bash

/opt/rh/rh-python36/root/usr/bin/python3 -m pip install --upgrade pip
/opt/rh/rh-python36/root/usr/bin/python3 -m pip install -r ../requirements.txt

# copy modules for new wsgi
sudo cp /opt/rh/httpd24/root/usr/lib64/httpd/modules/mod_rh-python36-wsgi.so /lib64/httpd/modules
sudo cp /opt/rh/httpd24/root/etc/httpd/conf.modules.d/10-rh-python36-wsgi.conf /etc/httpd/conf.modules.d
sudo systemctl restart httpd


sudo mkdir -p /var/www/mamlambo/html
sudo mkdir -p /var/www/mamlambo/wsgi
sudo mkdir -p /var/www/mamlambo/log

sudo chown -R $USER:$USER /var/www/mamlambo/html
# sudo chmod -R 755 /var/www

sudo bash -c "cat > /etc/httpd/conf.d/mamlambo.conf <<EOL
Listen $PORT
# create new
<VirtualHost *:$PORT>

    ServerName mamlambo
    DocumentRoot /var/www/mamlambo/html
    WSGIDaemonProcess mamlambo 
    WSGIProcessGroup mamlambo
    WSGIScriptAlias /mamlambo /var/www/mamlambo/wsgi/wsgi.py

    <Directory /var/www/mamlambo/html>
        Order allow,deny
        Allow from all
    </Directory>

    <Directory /var/www/mamlambo/wsgi>
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
EOL"

sudo systemctl restart httpd

firewall-cmd --zone=public --add-port=$PORT/tcp --permanent
firewall-cmd --reload

