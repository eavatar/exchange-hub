# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Avatar-specific functionality.
"""

import json
import logging
import falcon
from datetime import datetime
from cqlengine import columns
from cqlengine.models import Model

from eavatar.hub.app import api

from eavatar.hub import views
from eavatar.hub import managers
from eavatar.hub import hooks
from eavatar.hub.util import crypto, codecs

logger = logging.getLogger(__name__)


# models #
class Avatar(Model):
    """
    Represents anything with an identity that can send or receive messages.
    """
    xid = columns.Text(primary_key=True, partition_key=True)
    kind = columns.Text(default='thing')
    created_at = columns.DateTime(default=datetime.utcnow)
    modified_at = columns.DateTime(default=datetime.utcnow)
    content_length = columns.Integer(default=0)
    content_etag = columns.Text(default=None)
    content = columns.Text(default="")


class AvatarOwner(Model):
    """
    Represents relationship between an avatar and its owner.
    """
    owner_xid = columns.Text(primary_key=True)
    avatar_xid = columns.Text(primary_key=True, clustering_order="ASC")


# managers #
class AvatarManager(managers.BaseManager):
    model = Avatar

    def __init__(self):
        super(AvatarManager, self).__init__(self.model)


# views #
class AvatarCollection(views.ResourceBase):
    def on_get(self, req, resp):
        resp.body = views.EMPTY_LIST
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        Generates new Avatar without keep it in database.
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

    def on_put(self, req, resp):
        try:
            data = json.load(req.stream)
            avatar = Avatar(xid=data.get('xid'), kind=data.get('kind'))
            avatar.save()
            resp.body = views.RESULT_OK
            resp.status = falcon.HTTP_200
        except Exception, e:
            logger.error(e)
            raise


class AvatarResource(views.ResourceBase):

    def on_get(self, req, resp, avatar_xid):
        rs = Avatar.objects(xid=avatar_xid).limit(1)
        if len(rs) == 0:
            raise falcon.HTTPNotFound

        resp.body = json.dumps(rs[0])
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, avatar_xid):
        data = json.load(req.stream)
        data["xid"] = avatar_xid
        avatar = Avatar(xid=data.get('xid'), kind=data.get('kind'))
        avatar.save()
        resp.body = views.RESULT_OK
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, avatar_xid):
        pass


# routes
logger.debug("Binding routes for Avatar module.")
api.add_route("/avatars", AvatarCollection())
api.add_route("/avatars/{avatar_xid}", AvatarResource())
