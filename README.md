<img src="https://github.com/lhotakj/Mamlambo/raw/master/doc/assets/logo-big.png" width="60" align="right" />

<img src="https://github.com/lhotakj/Mamlambo/raw/master/doc/assets/title.png" width="250" />

[![CircleCI](https://circleci.com/gh/lhotakj/Mamlambo/tree/master.svg?style=svg)](https://circleci.com/gh/lhotakj/Mamlambo/tree/master) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Mamlambo&metric=alert_status)](https://sonarcloud.io/dashboard?id=Mamlambo) [![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/lhotakj/Mamlambo/graphs/commit-activity) 

[![DeepSource](https://static.deepsource.io/deepsource-badge-light.svg)](https://deepsource.io/gh/lhotakj/Mamlambo/?ref=repository-badge)

![Python 2.x](https://img.shields.io/badge/python&nbsp;2-no-red.svg) ![Python 3.4+](https://img.shields.io/badge/python&nbsp;3.4-yes-green.svg)

Mamlambo a full stack light weighted Python 3.4+ WSGI framework supporting easy templating, based on [Kajiki](https://github.com/nandoflorestan/kajiki/tree/master/kajiki). It's inspired by Microsoft .NET web-forms (web forms with master pages) and IIS configuration while also taking some Apache configuration concepts. The key features are as follows:

* Separated markup files with HTML code and code-behind file
* Master pages - for easy templating
* Serving of static content
* Mod_rewrite like rules for friendly URLs with redirection
* Fast handlers like in .NET - page without an HTML markup (in progress)
* Rich Kajiki templating syntax
* YAML based configuration

Mamlambo is an african sizeable snake-like creature. Locals state that it measures twenty meters in length and has a lower body of a fish, the head of a horse and the neck of a snake. 

## Requirements
- Python 3.4+
- WSGI server (Apache 2.4, Gunicorm, etc.) - demo provided on Apache 2.4

## Installation Instructions
* Download the latest stable release from GitHub (TBD) or install via pip `pip install Mamlambo` (TBD)
* Apache:
    * You wil need [**mod_wsgi**](https://github.com/GrahamDumpleton/mod_wsgi) developed by [Graham Dumpleton](https://github.com/GrahamDumpleton) to be able to run WSGI with Python3 - [follow the instructions how to compile mod_wsgi with Python 3.7.3](https://github.com/lhotakj/enable-wsgi_mod-python37-apache/blob/master/install.yaml) or you can you prepared [docker images](https://cloud.docker.com/u/lhotakj/repository/docker/lhotakj/centos-apache-mod_wsgi-python3), if you miss some specific version of Python, let me know, or you can build your own image by altering the [script](https://github.com/lhotakj/Mamlambo/tree/master/docker).
    * Prepare the WSGI application and place to your prefered path, e.g. `/var/www/wsgi`, see [demo files](https://github.com/lhotakj/Mamlambo/tree/master/demo/wsgi)
    * Add a the [following lines](https://raw.githubusercontent.com/lhotakj/Mamlambo/master/demo/apache/mamlambo.conf) to your `httpd.conf` file or preferably add [this file](https://github.com/lhotakj/Mamlambo/blob/master/demo/apache/mamlambo.conf) to the folder with configuration. Make sure the paths are correct.
    * Restart Apache daemon

## Basic concept
The framework is capable serving static content (`.jpg`, `.png`, `.ico` etc.), dynamic HTML content (by default markup `.pyhtml` extension with `.pyhtml.py` with code behind) and handlers (by default `.pyh` extension). The extensions are configurable in the yaml file. The configuration file has the following sections:

### 1. Static content
Extensions defined in the configuration with flag `serve: static` get served with defined MIME type as found on the file system under `DOCUMENT_ROOT`. If your `DOCUMENT_ROOT` is set to `/var/www/html/` and contains `favicon.ico` it gets served under `/favicon.ico` URL. In case you use can let Apache handle the static files.

### 2. Dynamic content with markup files
The simplest dynamic file can look like this file. The code should start with page directive `<%page %>`:

**demo.pyhtml**:
```html
<%page %>
<html><body>
<?python
import datetime 
now = str(datetime.datetime.now())
?>
Current data and time is <span py:content="now" />
</body></html>
```

Alternatively you can place you code to a code behind file

**demo.pyhtml.py**:
```python
import datetime 
now = str(datetime.datetime.now())
```

and in page directive of the markup file add a link to the codebehind file **demo.pyhtml**:
```html
<%page code=demo.pyhtml.py" %>
<html><body>
Current data and time is <span py:content="now" />
</body></html>
```

### 3. Dynamic content with master page
Firstly define your master page with a page directive `<%master %>`, this example has also a code behind python file. Use tags `py:placeholder>` to mark elements which will be replaced. Please note the the master page and the page using this master page has to contain the same IDs.

**master.pyhtml**:
```html
<%master code="master.pyhtml.py" %>
<!DOCTYPE html>
<html xmlns:py="http://www.w3.org/1999/xhtml">
<body>
-- HEADER --
<py:placeholder id="header"></py:placeholder>
-- HEADER --
-- CONTENT --
<py:placeholder id="content"></py:placeholder>
-- CONTENT --
</body>
</html>
```

**use_master.pyhtml**
```html
<%page masterpage="master.pyhtml" code="use_master.pyhtml.py" %>
<py:placeholder id="header">
 <span py:content="literal(master_name)" />
</py:placeholder>

<py:placeholder id="content">
this is my content from use_master page
</py:placeholder>

DEBUG: ${literal(debug)}<br />
  
Powered by Mamlambo: <span py:content="version" />
</py:placeholder>
```


### 4. Getting request object
To access the request details, instantiate an object of class `Request()` from `Mamlambo` namespace.
```python
from Mamlambo.Request import Request
request = Request()
# request.path_info ...... contains full relative URL
# request.method ......... "GET" | "POST" | "DELETE" ...
# request.query_string ... query string like `?param1=value1&param2=value2
```


### Configuration

```yaml
- extension: ".<extension>"
    serve: static | dynamic 
    mime: "<mimetype>"
    headers:
      - <header1-name>: <header1-value>
      - <header2-name>: <header2-value>
    methods:
      - GET 
      - POST
      - HEAD

```

