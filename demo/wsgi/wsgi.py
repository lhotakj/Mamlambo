#!/usr/bin/env python3

import sys
import os
from Mamlambo import Router

os.environ['MAMLAMBO_CONFIGURATION']='/var/www/mamlambo/wsgi/wsgi.configuration.yaml'

def application(environ, start_response):
    response = Router.Router(environ)
    start_response(response.status, response.headers)
    return response.content
