#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from .MamlamboException import MamlamboException


class RendererStatic:
    def __init__(self, config, request, response):
        response.complete = False

        # check first static stuff
        for extension_static in config.extensions_static:
            extension = list(extension_static)[0].lower()
            values = dict(extension_static).get(extension)
            if request.path_info.lower().endswith(extension):
                # static extension registered, now check the file system
                # remove first character as it's always / so join would not work
                expected_file_path = os.path.join(config.document_root, request.path_info.lstrip('/'))
                try:
                    with open(expected_file_path, "rb") as static_file_reader:
                        static_file_content = static_file_reader.read()
                        response.code = 200
                        response.content_bytes = static_file_content
                        response.mime = values["mime"]
                        response.add_header_from_config(values["headers"])
                        response.end()
                        return
                except Exception as e:
                    response_exception = MamlamboException.render(404,
                                                                  error="Page not found",
                                                                  description="The URL cannot be found.",
                                                                  details="Static file can't be read "
                                                                          "`{expected_file_path}`. "
                                                                  .format(expected_file_path=expected_file_path) + str(
                                                                      e))

                    response.code = response_exception.code
                    response.content_bytes = response_exception.content_bytes
                    response.mime = response_exception.mime
                    response.end()
                    return

        # check and check for dynamic stuff
        for extension_dynamic in config.extensions_dynamic:
            extension = list(extension_dynamic)[0].lower()
            print("extension_dy:" + extension)
            values = dict(extension_dynamic).get(extension)
            if request.path_info.lower().endswith(extension):
                # ok known
                return

        # something got wrong so return an error!
        response_exception = MamlamboException.render(404,
                                                      error="Page not found",
                                                      description="The URL is not recognized.",
                                                      details="The extension is not registered in the server. Please "
                                                              "check `extensions` section in your configuration.")
        response.code = response_exception.code
        response.content_bytes = response_exception.content_bytes
        response.mime = response_exception.mime
        response.end()
        return
