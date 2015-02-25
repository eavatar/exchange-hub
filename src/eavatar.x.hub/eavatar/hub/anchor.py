# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Anchor management.
"""

import ujson as json
import logging
import falcon
from cqlengine import columns
from cqlengine.models import Model

from .hooks import check_authentication
from eavatar.hub.app import api
from eavatar.hub.managers import BaseManager


logger = logging.getLogger(__name__)


class Anchor(Model):
    """
    Represents an outgoing link to an avatar or an endpoint.
    An anchor must belong to one and only one avatar.
    """
    avatar_xid = columns.Text(primary_key=True, partition_key=True)
    label = columns.Text(primary_key=True, clustering_order="ASC", default='')
    value = columns.Text()  # an url if kind is endpoint, or an XID for avatar.


class AnchorManager(BaseManager):
    model = Anchor

    def __init__(self):
        super(AnchorManager, self).__init__(Anchor)


class AnchorStore(object):

    def __init__(self, manager):
        self.manager = manager

    def on_get(self, req, resp, avatar_xid):
        logger.debug("Gets anchors for Avatar: %s", avatar_xid)
        qs = self.manager.find(avatar_xid=avatar_xid)
        result = []
        for item in qs:
            result.append(item)

        resp.body = json.dumps(result)

    def on_delete(self, req, resp, avatar_xid):
        qs = self.manager.find(avatar_xid=avatar_xid)
        qs.delete()

        resp.status = falcon.HTTP_204


class AnchorResource(object):

    def __init__(self, manager):
        self.manager = manager

    @falcon.before(check_authentication)
    def on_get(self, req, resp, avatar_xid, label=""):
        logger.debug("Gets anchor for Avatar: %s with label: %s", avatar_xid, label)
        result = self.manager.find_one(avatar_xid=avatar_xid, label=label)
        resp.body = json.dumps(result)

        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, avatar_xid, label=""):
        logger.debug("Updates anchor for Avatar: %s with label: %s", avatar_xid, label)
        pyobj = json.load(req.stream)
        pyobj["avatar_xid"] = avatar_xid
        self.manager.create(**pyobj)

    def on_delete(self, req, resp, avatar_xid, label=""):
        logger.debug("Removes anchor for Avatar: %s with label: %s", avatar_xid, label)
        qs = self.manager.find(avatar_xid=avatar_xid, label=label)
        qs.delete()

        resp.status = falcon.HTTP_204


_manager = AnchorManager()

# routes
api.add_route("/avatars/{avatar_xid}/anchors", AnchorStore(_manager))
api.add_route("/avatars/{avatar_xid}/anchors/{label}", AnchorResource(_manager))