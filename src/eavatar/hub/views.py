# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import falcon


class RootView(object):
    def on_get(self, req, resp):
        resp.body = '{"message": "Hello from root!"}'
        resp.status = falcon.HTTP_200


class AvatarView(object):

    def on_get(self, req, resp):
        resp.body = '{"message": "Hello from avatar!"}'
        resp.status = falcon.HTTP_200


class AnchorView(object):
    def on_get(self, req, resp):
        resp.body = '{"message": "Hello from anchor!"}'
        resp.status = falcon.HTTP_200
