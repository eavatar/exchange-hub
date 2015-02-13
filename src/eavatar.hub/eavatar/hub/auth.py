# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Functions relating to authentication and security tokens.
"""

import base58
import falcon
import ujson as json
from eavatar.hub import views
from eavatar.hub import util


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


