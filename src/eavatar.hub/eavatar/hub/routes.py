# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Map URI routes to resources(views).
"""

from eavatar.hub.app import api
from eavatar.hub import (
    webroot, avatar, auth, anchor, message, status, router,
)

from eavatar.hub.sinks.static import StaticFiles

#
# resource mappings.
#
api.add_route("/", webroot.RootResource())
api.add_route("/favicon.ico", webroot.FaviconResource())

api.add_route("/status", status.StatusResource())

api.add_route("/avatars", avatar.AvatarCollection())
api.add_route("/avatars/{avatar_xid}", avatar.AvatarResource())
api.add_route("/avatars/{avatar_xid}/messages", message.MessageStore())

api.add_route("/route/{address}", router.RouterResource())

api.add_route("/keypair", auth.KeypairResource())

#
# sinks
#

# serves static files
api.add_sink(StaticFiles(), '/static')
