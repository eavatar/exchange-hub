# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Avatar-specific functionality.
"""

import json
import time
import logging
import falcon
from datetime import datetime, timedelta
from cqlengine import columns
from cqlengine.models import Model

from eavatar.hub.app import api

from eavatar.hub import views
from eavatar.hub import managers
from eavatar.hub.hooks import check_authentication
from eavatar.hub.util import crypto, codecs

logger = logging.getLogger(__name__)


def _default_expired_at():
    return datetime.utcnow() + timedelta(seconds=86400)


# models #
class Avatar(Model):
    """
    Represents anything with an identity that can send or receive messages.
    """
    xid = columns.Text(primary_key=True, partition_key=True)
    owner_xid = columns.Text(default=None)
    created_at = columns.DateTime(default=datetime.utcnow)
    modified_at = columns.DateTime(default=datetime.utcnow)
    expired_at = columns.DateTime(default=_default_expired_at)
#    properties = columns.Map(columns.Text, columns.Text)
#    links = columns.Set(columns.Text)
#    aliases = columns.Set(columns.Text)


class Possession(Model):
    """
    Represents relationship between an avatar and its possessions.
    """
    owner_xid = columns.Text(primary_key=True)
    avatar_xid = columns.Text(primary_key=True, clustering_order="ASC")

    @staticmethod
    def find_possessions(owner_xid):
        return Possession.objects(owner_xid=owner_xid)


# managers #
class AvatarManager(managers.BaseManager):
    model = Avatar

    def __init__(self):
        super(AvatarManager, self).__init__(self.model)


# views #
@falcon.before(check_authentication)
class AvatarCollection(views.ResourceBase):
    def on_get(self, req, resp):
        """
        Gets avatars belongs to the client.

        :param req:
        :param resp:
        :return:
        """
        owner_xid = req.context['client_xid']
        qs = Possession.find_possessions(owner_xid)
        resp.body = views.EMPTY_LIST
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


@falcon.before(check_authentication)
class AvatarResource(views.ResourceBase):

    def on_get(self, req, resp, avatar_xid):
        if 'self' == avatar_xid:
            avatar_xid = req.context['client_xid']

        rs = Avatar.objects(xid=avatar_xid).limit(1)
        if len(rs) == 0:
            raise falcon.HTTPNotFound

        resp.body = json.dumps(rs[0])
        resp.status = falcon.HTTP_200

    def on_patch(self, req, resp, avatar_xid):
        """
        Patches the avatar.

        :param req:
        :param resp:
        :param avatar_xid:
        :return:
        """
        if 'self' == avatar_xid:
            avatar_xid = req.context['client_xid']


    def on_put(self, req, resp, avatar_xid):
        """
        Replaces the avatar with new content.

        :param req:
        :param resp:
        :param avatar_xid:
        :return:
        """
        client_xid = req.context['client_xid']
        if 'self' == avatar_xid:
            avatar_xid = client_xid

        data = json.load(req.stream)
        data["xid"] = avatar_xid
        avatar = Avatar(xid=data.get('xid'), owner_xid=client_xid)
        avatar.save()
        resp.body = views.RESULT_OK
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, avatar_xid):
        if 'self' == avatar_xid:
            avatar_xid = req.context['client_xid']

        Avatar.objects(avatar_xid=avatar_xid).delete()
        resp.status = falcon.HTTP_204



# routes

logger.debug("Binding routes for Avatar module.")

_avatar_resource = AvatarResource()
api.add_route("/{avatar_xid}", _avatar_resource)
