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
from eavatar.hub.util import crypto, codecs

logger = logging.getLogger(__name__)


class AuthResource(views.ResourceBase):

    def on_post(self, req, resp):
        """
        Generates new keypair.
        :param req:
        :param resp:
        :return:
        """
        jsonobj = json.load(req.stream)
        salt = str(jsonobj["salt"])
        password = str(jsonobj["password"])
        logger.debug("Generating new avatar from salt: %s, password: %s", salt, password)

        seed = crypto.derive_secret_key(password=password, salt=salt)
        (pk, sk) = crypto.generate_keypair(sk=seed)
        result = dict()
        result["xid"] = crypto.key_to_xid(pk)
        result["key"] = codecs.base58_encode(pk)
        result["secret"] = codecs.base58_encode(sk)

        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200


logger.debug("Binding routes for Auth module...")
# routes
api.add_route("/key", AuthResource())
