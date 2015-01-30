# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


class SinkBase(object):
    def __init__(self, context=None):
        self._context = context

    def __call__(self, req, resp, *args, **kwargs):
        self.handle(req, resp, **kwargs)

    def handle(self, req, resp, kwargs):
        pass