[![CircleCI](https://circleci.com/gh/lhotakj/Mamlambo/tree/master.svg?style=svg)](https://circleci.com/gh/lhotakj/Mamlambo/tree/master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Mamlambo&metric=alert_status)](https://sonarcloud.io/dashboard?id=Mamlambo)

<img src="https://github.com/lhotakj/Mamlambo/raw/master/doc/assets/logo-big.png" width="120" />

# <img src="https://github.com/lhotakj/Mamlambo/raw/master/doc/assets/title.png" width="210" /> 
Mamlambo is an african sizeable snake-like creature. Locals state that it measures twenty meters in length and has a lower body of a fish, the head of a horse and the neck of a snake.

## Requirements
- Python 3.4+
- WSGI server (Apache 2.4, Gunicorm, etc.) - demo provided on Apache 2.4

## Installation Instructions
* Download the latest stable release from GitHub (TBD) or install via pip `pip install Mamlambo` (TBD)
* Apache:
    * [follow the instructions how to compile mod_wsgi with Python 3.7.3](https://github.com/lhotakj/enable-wsgi_mod-python37-apache/blob/master/install.yaml)
    * Prepare the WSGI application and place to your prefered path, e.g. `/var/www/wsgi`, see (demo files)[https://github.com/lhotakj/Mamlambo/tree/master/demo/wsgi]
    * Add a the (following lines)[https://raw.githubusercontent.com/lhotakj/Mamlambo/master/demo/apache/mamlambo.conf] to your `httpd.conf` file or preferably add (this file)[https://github.com/lhotakj/Mamlambo/blob/master/demo/apache/mamlambo.conf] to the folder with configuration. Make sure the paths are correct.
    * Restart Apache daemon


