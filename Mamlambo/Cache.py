#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from . import Session as session
from . import Singleton


@Singleton.singleton_object
class Cache(metaclass=Singleton.Singleton):
    __data = {}  # {:url": {content}

    def __init__(self):
        self.__data = {}  # { 'default': {"key1":[ exp1, value1]}, 'domain2': {"key1":[ exp1, value1] }

    def set(self, url, content, headers, status, exp=None):
        self.__data[url] = (content, headers, status, exp)

    def get(self, url):
        if url in self.__data:
            (content, headers, status, exp) = self.__data[url]
            return content, headers, status
        else:
            return None
