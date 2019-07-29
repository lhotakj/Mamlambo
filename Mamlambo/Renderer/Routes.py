#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

from enum import Enum


class Mode(Enum):
    redirection = 'redirection'  # permanent 301
    route = 'route'


class Routes:

    # mode = 'redirection' adds header Location and response.end
    # mode = 'route' changes url
    # example - keep in mind ${1} must be in {}!
    #  "^/services/web/jira/(.*)/(.*)$": "/jira.pyhtml?x=${1}&y=${2}"
    def __init__(self, section, request, response, mode):
        if section:
            for old, new in section.items():
                matches = re.findall(old, request.uri)
                if matches:
                    new_url = new
                    new_url = new_url.replace("${0}", request.uri)
                    loop = 1
                    matches = matches[0]
                    for m in matches:
                        ch = m.replace("&", "%26")
                        new_url = new_url.replace(("${" + str(loop) + "}"), ch)
                        loop = loop + 1

                    url_parts = new_url.split("?", 1)
                    if mode == Mode.route:
                        if len(url_parts) > 1:
                            request.query_string = url_parts[1]
                            request.path_info = url_parts[0]
                        else:
                            request.query_string = None
                            request.path_info = new_url

                        request.uri = new_url

                    if mode == Mode.redirection:
                        response.add_header("Location", new_url)
                        response.code = 301
                        response.end()

