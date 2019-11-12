#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Mamlambo.Renderer import Dynamic, Default, Static
from Mamlambo.Renderer.Routes import Routes
from Mamlambo.Renderer.Routes import Mode
from Mamlambo.Core.Configuration import Configuration
from Mamlambo.Response import Response
from Mamlambo import Request
from Mamlambo.Core.MamlamboException import MamlamboException
from Mamlambo.Core.Cache import Cache


class Router:
    __response = None
    __headers = []
    __content = ""
    __status = None

    def __init__(self, env, path_to_configuration=None):

        response = Response()  # instantiate empty singleton
        response.complete = False
        # Singleton.Singleton.reset(response)

        # read the yaml configuration and fill request singleton
        config = Configuration()  # instantiate empty singleton, persistent

        internal_cache = False
        if internal_cache:
            cache = Cache()

        # load only first time
        if not config.loaded:
            exception_response = config.parse_config(env, path_to_configuration)
            if isinstance(exception_response, Response):
                self.__content = [exception_response.content_bytes]
                self.__headers = exception_response.headers_render
                self.__status = exception_response.status
                return

        request = Request.Request()
        exception_response = config.parse_request(env, request)
        if isinstance(exception_response, Response):
            self.__content = [exception_response.content_bytes]
            self.__headers = exception_response.headers_render
            self.__status = exception_response.status
            return

        if internal_cache:
            cached_object = cache.get(request.uri)
            if cached_object:
                (cached_content, cached_headers, cached_status) = cached_object
                self.__content = cached_content
                self.__headers = cached_headers
                self.__status = cached_status
                return

        # process request ---------------------------------------------------------------------------------------
        # 1) check redirections
        Routes(config.redirections, request, response, Mode.redirection)
        if response.complete:
            self.__content = [b'']
            self.__headers = response.headers_render
            self.__status = response.status
            if internal_cache:
                cache.set(url=request.uri, content=[response.content_bytes], headers=response.headers,
                          status=response.status)
            return

        # 2) check routes
        Routes(config.routes, request, response, Mode.route)

        # 3) check default document
        Default.Default(config, request, response)
        if response.complete:
            self.__content = [response.content_bytes]
            self.__headers = response.headers_render
            self.__status = response.status
            if internal_cache:
                cache.set(url=request.uri, content=[response.content_bytes], headers=response.headers,
                          status=response.status)
            return

        # 4) check static content
        Static.Static(config, request, response)
        if response.complete:
            self.__content = [response.content_bytes]
            self.__headers = response.headers_render
            self.__status = response.status
            if internal_cache:
                cache.set(url=request.uri, content=[response.content_bytes], headers=response.headers,
                          status=response.status)
            return

        #print('--after-statisc --')
        #print("response.content=" + str(response.content_bytes))
        #print("response.complete=" + str(response.complete))
        #print("response.status=" + str(response.status))

        Dynamic.RendererMain(request, response)
        if response.complete:
            self.__content = [response.content_bytes]
            self.__headers = response.headers_render
            self.__status = response.status
            return
        else:
            response = MamlamboException.render(
                http_code=404,
                error="Page not found",
                details="The requested resource is not available. Please try to navigate back to the homepage")
            self.__content = [response.content_bytes]
            self.__headers = response.headers_render
            self.__status = response.status

        return

    # properties to pass data to WSGI
    @property
    def headers(self):
        return self.__headers

    @property
    def content(self):
        return self.__content

    @property
    def status(self):
        return self.__status

# render = Renderer("template.html")
# render = Renderer("use_master.html")

# print(loader.page_result)

# print(render.page_result)
# print(render.page_mime)
# print(render.http_code)
