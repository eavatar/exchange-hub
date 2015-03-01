# -*- coding: utf-8 -*-
"""
Base class/interfaces for sinks.
"""
from __future__ import absolute_import, division, print_function, unicode_literals


class SinkBase(object):
    """
    Base class for sinks.
    """
    def __init__(self, context=None):
        self._context = context

    def __call__(self, req, resp, *args, **kwargs):
        self.handle(req, resp, **kwargs)

    def handle(self, req, resp, kwargs):
        """
        Invoked to handle request. Do nothing by default, should be overridden by subclasses.
        :param req:
        :param resp:
        :param kwargs:
        :return:
        """
        pass
