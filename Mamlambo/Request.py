#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from Mamlambo.Session import Session
import inspect
import os
import pickle


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

    __get = None

    __master = None
    __obj = None

    def __init__(self, headers=None, ):

        frame = inspect.stack()[1][0]
        #print('!!-----------')
        #print(str(dir(frame)))
        #print(str(frame.f_locals))
        #print('!!-----------')

        if "_REQUEST" in frame.f_locals:
            # self.url = frame.f_locals["__REQUEST"].url
            # self.method = frame.f_locals["__REQUEST"].method
            obj = pickle.loads(frame.f_locals["_REQUEST"])
            self.__obj = obj
            #obj = frame.f_locals["_REQUEST"]
            for variable in dir(self):
                if not variable.startswith('_'):
                    try:
                        setattr(Request, variable, obj.__getattribute__(variable))
                        #print(variable + "=" + obj.__getattribute__(variable))
                    except:
                        pass
        if headers:
            self.__headers = headers

#    def __repr__(self):
#        return str(self.__obj)

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
        return self.__session.keys if self.__session else None

    @property
    def session_id(self):
        return str(self.__session.session_id) if self.__session else None

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

    @get.setter
    def get(self, value):
        self.__param_get = value

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
