# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

"""
Map URI routes to resources(views).
"""

from .app import api
from .views import (
    RootResource,
    FaviconResource,
    AvatarCollection,
    AvatarResource,
    RouterResource,
    KeypairResource,
    StatusResource,
)

from .sinks.static import StaticFiles

#
# resources
#
api.add_route("/", RootResource())
api.add_route("/favicon.ico", FaviconResource())
api.add_route("/status", StatusResource())
api.add_route("/avatars", AvatarCollection())
api.add_route("/avatars/{avatar_xid}", AvatarResource())
api.add_route("/route/{address}", RouterResource())
api.add_route("/keypair", KeypairResource())

#
# sinks
#

# serves static files
api.add_sink(StaticFiles(), '/static')
