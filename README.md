<img src="https://github.com/lhotakj/Mamlambo/raw/master/doc/assets/title.png" width="210" />

[![CircleCI](https://circleci.com/gh/lhotakj/Mamlambo/tree/master.svg?style=svg)](https://circleci.com/gh/lhotakj/Mamlambo/tree/master)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Mamlambo&metric=alert_status)](https://sonarcloud.io/dashboard?id=Mamlambo)

<img src="https://github.com/lhotakj/Mamlambo/raw/master/doc/assets/logo-big.png" width="14" align="right" />
Mamlambo a full stack light weighted Python 3.4+ WSGI framework supporting easy templating, based on (Kajiki)[https://github.com/nandoflorestan/kajiki/tree/master/kajiki]. It's inspired by Microsoft .NET web-forms (web forms with master pages) and IIS configuration while also taking some Apache configuration concepts. The key features are as follows:
* Separated markup files with HTML code and code-behind file
* Master pages - for easy templating
* Serving of static content
* Mod_rewrite like rules for friendly URLs with redirection
* Fast handlers like in .NET - page without an HTML markup (in progress)
* Rich Kajiki syntax
* YAML based configuration

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


