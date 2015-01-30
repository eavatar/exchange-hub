# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

"""
Map URI routes to resources(views).
"""

from .app import api
from .views import RootView, AvatarView, AnchorView, FaviconResource
from .sinks.static import StaticFiles

# resources
api.add_route("/", RootView())
api.add_route("/favicon.ico", FaviconResource())
api.add_route("/avatars", AvatarView())
api.add_route("/anchors", AnchorView())

# sinks
api.add_sink(StaticFiles(), '/static')
