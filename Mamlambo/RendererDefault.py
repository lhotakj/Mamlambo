#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from .MamlamboException import MamlamboException


class RendererDefault:

    def __init__(self, config, request, response):

        if request.path_info.endswith("/"):
            map_path = os.path.join(config.document_root, request.path_info.lstrip('/'))
            if self.check_path(map_path, config, request):
                return
            else:
                response_exception = MamlamboException.render(404,
                                                              error="Page not found",
                                                              description="Do default document.",
                                                              details="The folder `{path_info}` doesn't contain "
                                                                      "a default document, check `default_document` "
                                                                      "section in your configuration.".
                                                              format(path_info=map_path))
                response.code = response_exception.code
                response.content_bytes = response_exception.content_bytes
                response.mime = response_exception.mime
                response.end()
                return

        else:
            if config.trailing_slash_redirect:
                # try trailing slash
                path_info_with_slash = request.path_info + "/"
                map_path = os.path.join(config.document_root, path_info_with_slash.lstrip('/'))
                if os.path.exists(map_path) and os.path.isdir(map_path):
                    if self.check_path(map_path, config, request):
                        response.content_str = ""
                        new_url = path_info_with_slash if not request.query_string else \
                            path_info_with_slash + "?" + request.query_string
                        print("redir to: " + new_url)
                        response.add_header("Location", new_url)
                        response.code = 301
                        response.end()
                        return
                    else:
                        response_exception = MamlamboException.render(404,
                                                                      error="Page not found",
                                                                      description="Do default document.",
                                                                      details="The folder `{path_info}` doesn't contain "
                                                                              "a default document, check `default_document` "
                                                                              "section in your configuration.".
                                                                      format(path_info=map_path))
                        response.code = response_exception.code
                        response.content_bytes = response_exception.content_bytes
                        response.mime = response_exception.mime
                        response.end()
                        return

    def check_path(self, map_path, config, request):
        for document in config.default_document:
            map_path_document = os.path.join(map_path, document)
            if os.path.exists(map_path_document) and os.path.isfile(map_path_document):
                request.path_info += "/" + document
                return True
        return False
