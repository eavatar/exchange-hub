# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import falcon
from eavatar.hub.util import webutils

logger = logging.getLogger(__name__)


def nocache(req, resp, params):
    resp.set_header(b'pragma', b'no-cache')
    resp.set_header(b'cache-control', b'no-cache')


def static_cacheable(req, resp):
    resp.set_header(b'cache-control', b'max-age=86400,s-maxage=86400')


def set_cors_header(req, resp):
    """
    Set response header for allowing access from any origins.

    :param req:
    :param resp:
    :return:
    """
    resp.set_header(b'Access-Control-Allow-Origin', '*')


class RootResource(object):
    def on_head(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        logger.debug(req.get_header(b'accept'))
        prefered_type = req.client_prefers([b'text/html', b'application/json'])
        if prefered_type == b'application/json':
            resp.status = falcon.HTTP_200
            resp.body = b'{"message": "Hello from root!"}'
        else:
            webutils.send_static_file(req, resp, 'index.html', media_type=b'text/html; charset=utf-8')

@falcon.after(static_cacheable)
class FaviconResource(object):
    def __init__(self, *args, **kwargs):
        super(FaviconResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        webutils.send_static_file(req, resp, 'favicon.ico', media_type=b'image/vnd.microsoft.icon')


class StatusResource(object):
    """
    Check the service status.
    """
    def on_get(self, req, resp):
        resp.body = '{"result": "OK"}'
        resp.status = falcon.HTTP_200


class AvatarCollection(object):
    def on_get(self, req, resp):
        resp.body = '[]'
        resp.status = falcon.HTTP_200


class AvatarResource(object):

    def on_get(self, req, resp, avatar_xid):
        resp.body = '[{}]'
        resp.status = falcon.HTTP_200


class RouterResource(object):
    def on_post(self, req, resp, address=""):
        """
        Routes a message to its destination.

        :param req:
        :param resp:
        :return:
        """
        resp.status = falcon.HTTP_200