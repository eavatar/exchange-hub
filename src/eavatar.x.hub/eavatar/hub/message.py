# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Module for message manipulation.
"""

import json
import logging
import falcon
from cqlengine import columns
from cqlengine.models import Model
from eavatar.hub.app import api

from eavatar.hub.views import ResourceBase
from eavatar.hub.managers import BaseManager

logger = logging.getLogger(__name__)


class Message(Model):
    """
    Represents messages received by an avatar. A message consists of:
    * a headers
      Contains metadata regarding the payload. Some well-known headers are:
      - 'Content-type': the content type of the payload, e.g. 'application/json'.
      - 'Content-length': the length in bytes of the payload
      - 'Destination': the resource intended to be the receiver on final target.
    * a payload(optional)
      The content to be sent as is. That is, the hub doesn't interpret or modify the payload.

    """
    avatar_xid = columns.Text(primary_key=True, partition_key=True)
    message_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    headers = columns.Text()
    payload = columns.Text(default=None)


class MessageManager(BaseManager):
    model = Message

    def __init__(self):
        super(MessageManager, self).__init__(Message)


class MessageStore(ResourceBase):

    def on_get(self, req, resp, avatar_xid):
        """
        Gets last N messages of the specified avatar.

        :param req:
        :param resp:
        :param avatar_xid: the avatar's XID.
        :return:
        """
        qs = Message.objects(avatar_xid=avatar_xid).limit(10)
        result = []
        for m in qs:
            result.append(m)

        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200


logger.debug("Binding routes for Message module...")

# routes
api.add_route("/avatars/{avatar_xid}/messages", MessageStore())
