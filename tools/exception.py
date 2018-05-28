#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Error(Exception):
    def __init__(self, message=None):
        super(Error, self).__init__(message)

class NotFound(Error):
    pass

class ReqError(Error):
    pass

class Duplicate(Error):
    pass

class NotAuthorized(Error):
    pass

class NotEmpty(Error):
    pass

class Invalid(Error):
    pass

class InvalidInputException(Error):
    pass


class TimeoutException(Error):
    pass

class ExecuteError(Error):
    pass

class DBError(Error):
    """Wraps an implementation specific exception"""
    def __init__(self, inner_exception):
        self.inner_exception = inner_exception
        super(DBError, self).__init__(str(inner_exception))
