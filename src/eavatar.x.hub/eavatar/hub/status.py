# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import falcon
from eavatar.hub.app import api

from eavatar.hub import views

logger = logging.getLogger(__name__)


class StatusResource(views.ResourceBase):
    """
    Check the service status.
    """
    def on_get(self, req, resp):
        resp.body = views.RESULT_OK
        resp.status = falcon.HTTP_200

logger.debug("Binding routes for Status module...")
# routes
api.add_route("/.status", StatusResource())
