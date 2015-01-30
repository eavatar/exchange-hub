# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import falcon
from eavatar.hub.util import webutils

logger = logging.getLogger(__name__)


def nocache(req, resp, params):
    resp.set_header('pragma', 'no-cache')
    resp.set_header('cache-control', 'no-cache')


def static_cacheable(req, resp):
    resp.set_header('cache-control', 'max-age=86400,s-maxage=86400')


def set_cors_header(req, resp):
    """
    Set response header for allowing access from any origins.

    :param req:
    :param resp:
    :return:
    """
    resp.set_header('Access-Control-Allow-Origin', '*')


class RootView(object):
    def on_head(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        logger.debug(req.get_header('accept'))
        prefered_type = req.client_prefers(['text/html', b'application/json'])
        if prefered_type == 'application/json':
            resp.status = falcon.HTTP_200
            resp.body = '{"message": "Hello from root!"}'
        else:
            webutils.send_static_file(req, resp, 'index.html', media_type=b'text/html; charset=utf-8')

@falcon.after(static_cacheable)
class FaviconResource(object):
    def __init__(self, *args, **kwargs):
        super(FaviconResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        webutils.send_static_file(req, resp, 'favicon.ico', media_type='image/vnd.microsoft.icon')


class AvatarView(object):

    def on_get(self, req, resp):
        resp.body = '{"message": "Hello from avatar!"}'
        resp.status = falcon.HTTP_200


class AnchorView(object):
    def on_get(self, req, resp):
        resp.body = '{"message": "Hello from anchor!"}'
        resp.status = falcon.HTTP_200
