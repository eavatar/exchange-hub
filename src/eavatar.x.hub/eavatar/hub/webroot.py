# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Webroot
"""

import logging
import falcon
from eavatar.hub.app import api
from eavatar.hub import views
from eavatar.hub import util
from eavatar.hub import hooks

from eavatar.hub.sinks.static import StaticFiles


logger = logging.getLogger(__name__)


class RootResource(views.ResourceBase):
    def on_head(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        logger.debug(req.get_header(b'accept'))
        prefered_type = req.client_prefers([b'text/html', b'application/json'])
        if prefered_type == b'application/json':
            resp.status = falcon.HTTP_200
            resp.body = b'{"message": "Hello from root!"}'
        else:
            util.webutils.send_static_file(req, resp, 'index.html', media_type=b'text/html; charset=utf-8')


@falcon.after(hooks.static_cacheable)
class FaviconResource(object):
    def __init__(self, *args, **kwargs):
        super(FaviconResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        util.webutils.send_static_file(req, resp, b'favicon.ico', media_type=b'image/vnd.microsoft.icon')



logger.debug("Binding routes for Webroot module...")
# routes
index = RootResource()
api.add_route(b"/", index)
api.add_route(b"/index.html", index)
api.add_route(b"/favicon.ico", FaviconResource())


# serves static files
api.add_sink(StaticFiles(), b'/static')
