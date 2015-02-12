# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Map URI routes to resources(views).
"""

from eavatar.hub.app import api
from eavatar.hub import views

from eavatar.hub.sinks.static import StaticFiles

#
# resource mappings.
#
api.add_route("/", views.RootResource())
api.add_route("/favicon.ico", views.FaviconResource())

api.add_route("/status", views.StatusResource())

api.add_route("/avatars", views.AvatarCollection())
api.add_route("/avatars/{avatar_xid}", views.AvatarResource())
api.add_route("/avatars/{avatar_xid}/messages", views.MessageStore())

api.add_route("/route/{address}", views.RouterResource())

api.add_route("/keypair", views.KeypairResource())

#
# sinks
#

# serves static files
api.add_sink(StaticFiles(), '/static')
