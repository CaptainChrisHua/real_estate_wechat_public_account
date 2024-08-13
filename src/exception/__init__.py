# -*- coding:utf-8 -*-


class ParamException(Exception):

    def __init__(self, message) -> None:
        self.message = message


class NoCompanyException(Exception):

    def __init__(self, message: object):
        self.message = message


class NoDataException(Exception):

    def __init__(self, message: object):
        self.message = message
