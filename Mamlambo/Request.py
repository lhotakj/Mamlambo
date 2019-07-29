#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from Mamlambo.Session import Session
import inspect

import os

REQUEST = None

class Request():
    __headers = []
    __session = None
    __app_id = None
    __param_get = None
    __param_post = None
    __param_json = None
    __method = None
    __scheme = None
    __uri = None
    __path_info = None
    __query_string = None

    __master = None

    def __init__(self, headers=None, ):
        global REQUEST

        print(REQUEST)
        #print(str(frame.f_globals))
        #print(str(frame.f_locals))

        #print("================================")
        #print("== LOCALS ==============================")
        #print(frame.f_back.f_locals)
        #print("================================")
        #print(frame.f_back.f_locals)

        #print(str(dir(self)))
        #print(str(globals()))
        #print(str(locals()))
        #print(str(globals()["request"]))
        #self.__uri = request.uri
        #o = urlparse(self.__uri)
        #self.__path_info = o.path
        if headers:
            self.__headers = headers

    def add_header(self, header, value):
        self.__headers = self.__headers + [(header, value)]

    def header(self, header_name):
        return dict(self.__headers).get(header_name)

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        self.__headers = value

    def session_start(self):
        self.__session = Session.Session()
        self.__session.start()

    @property
    def session(self):
        return self.__session.keys

    @property
    def session_id(self):
        return str(self.__session.session_id)

    def session_destroy(self):
        self.__session.destroy()
        self.__session = None

    @property
    def app_id(self):
        return self.__app_id

    @property
    def master(self):
        return self.__master

    @property
    def get(self):
        return self.__param_get

    @property
    def post(self):
        return self.__param_post

    @property
    def json(self):
        return self.__param_json

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, value):
        self.__method = value

    @property
    def scheme(self):
        return self.__scheme

    @scheme.setter
    def scheme(self, value):
        self.__scheme = value

    @property
    def uri(self):
        return self.__uri

    @uri.setter
    def uri(self, value):
        self.__uri = value

    @property
    def path_info(self):
        return self.__path_info

    @path_info.setter
    def path_info(self, value):
        self.__path_info = value

    @property
    def query_string(self):
        return self.__query_string

    @query_string.setter
    def query_string(self, value):
        self.__query_string = value
