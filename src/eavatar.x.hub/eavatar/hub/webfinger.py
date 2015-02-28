# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging
import falcon
from eavatar.hub import app
from eavatar.hub import views

from eavatar.hub import util


logger = logging.getLogger(__name__)

_X_AVATAR = b"x-avatar"
_JRD_TYPE = b"application/jrd+json"


class WebFinger(views.ResourceBase):

    def get_avatar_id(self, req):
        resource = req.get_param("resource", required=True)
        if not util.validate_xid(resource):
            logger.debug("Invalid XID: %s", resource)
            raise falcon.HTTPBadRequest("Resource parameter malformed", "Resource should be a valid Avatar XID.")
        return resource

    def on_options(self, req, resp):
        resp.set_header(b"Allow", b"HEAD,GET,OPTIONS")
        resp.status = falcon.HTTP_200

    def on_head(self, req, resp):
        avatar_xid = self.get_avatar_id(req)
        resp.set_header(_X_AVATAR, avatar_xid)
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        avatar_xid = self.get_avatar_id(req)

        base_uri, _ = req.uri.split("/.wellknown")

        messages_link = {
            "rel": "messages",
            "href": "%s/%s/messages" % (base_uri, avatar_xid),
        }

        result = dict(
            subject=avatar_xid,
            aliases=["%s/%s" % (base_uri, avatar_xid)],
            links=[messages_link],
        )

        resp.content_type = _JRD_TYPE
        resp.data = json.dumps(result)
        resp.set_header(_X_AVATAR, avatar_xid)
        resp.status = falcon.HTTP_200


# routes
_webfinger = WebFinger()
app.add_route(b"/.wellknown/webfinger", _webfinger)