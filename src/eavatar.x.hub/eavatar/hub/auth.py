# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Functions relating to authentication and security tokens.
"""

import base58
import logging
import falcon
import json
from eavatar.hub.app import api

from eavatar.hub import views
from eavatar.hub import util

logger = logging.getLogger(__name__)


class KeypairResource(views.ResourceBase):

    def on_post(self, req, resp):
        """
        Generates new keypair.
        :param req:
        :param resp:
        :return:
        """
        key, secret = util.crypto.generate_keypair()
        result = {}
        result['key'] = base58.b58encode(key)
        result['secret'] = base58.b58encode(secret)
        result['xid'] = util.crypto.key_to_xid(key)
        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200


logger.debug("Binding routes for Auth module...")
# routes
api.add_route("/keypair", KeypairResource())
