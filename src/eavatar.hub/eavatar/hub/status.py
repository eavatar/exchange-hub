# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import falcon
from eavatar.hub import views


class StatusResource(views.ResourceBase):
    """
    Check the service status.
    """
    def on_get(self, req, resp):
        resp.body = views.RESULT_OK
        resp.status = falcon.HTTP_200

