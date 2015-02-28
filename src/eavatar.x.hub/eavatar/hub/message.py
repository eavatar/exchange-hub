# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Module for message manipulation.
"""

import json
import uuid
import logging
import falcon
from cqlengine import columns
from cqlengine.models import Model
from eavatar.hub.app import api
from .hooks import check_authentication
from eavatar.hub.views import ResourceBase
from eavatar.hub.managers import BaseManager

logger = logging.getLogger(__name__)


def _new_msg_id():
    return bytes(uuid.uuid1())


class Message(Model):
    """
    Represents messages received by an avatar. A message consists of:
    * a headers
      Contains metadata regarding the payload. Some well-known headers are:
      - 'Content-type': the content type of the payload, e.g. 'application/json'.
      - 'Content-length': the length in bytes of the payload
    * a payload(optional)
      The content to be sent as is. That is, the hub doesn't interpret or modify the payload.

    """
    avatar_xid = columns.Text(primary_key=True, partition_key=True)
    message_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    headers = columns.Text()
    payload = columns.Text(default=None)

    def to_json(self):
        result = dict()
        result['headers'] = json.loads(self.headers)
        result['payload'] = self.payload
        return result


class MessageManager(BaseManager):
    model = Message

    def __init__(self):
        super(MessageManager, self).__init__(Message)


@falcon.before(check_authentication)
class MessageStore(ResourceBase):
    def __init__(self, manager):
        super(MessageStore, self).__init__()
        self.manager = manager

    def on_get(self, req, resp, avatar_xid):
        """
        Gets last N messages of the specified avatar.

        :param req:
        :param resp:
        :param avatar_xid: the avatar's XID.
        :return:
        """
        client_xid = req.context['client_xid']
        if "self" == avatar_xid:
            avatar_xid = client_xid

        if client_xid != avatar_xid:
            logger.debug("Access denied: client_xid: %s, avatar_xid: %s", client_xid, avatar_xid)
            raise falcon.HTTPForbidden(title="Forbidden", description="Can only retrieve own messages.")

        marker = req.get_param('marker')
        limit = req.get_param_as_int('limit', min=1, max=100)
        if limit < 0:
            limit = 1
        if marker:
            qs = Message.objects(avatar_xid=avatar_xid, message_id__gt=marker).limit(limit)
        else:
            qs = Message.objects(avatar_xid=avatar_xid).limit(limit)

        result = []
        for m in qs:
            result.append(m.to_json())

        resp.data = json.dumps(result)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, avatar_xid):
        client_xid = req.context['client_xid']
        if "self" == avatar_xid:
            avatar_xid = client_xid

        data = json.load(req.stream)
        headers = data.get('headers', {})
        msg_id = _new_msg_id()
        headers['message_id'] = msg_id
        headers['from'] = client_xid
        headers['to'] = avatar_xid
        Message.create(avatar_xid=avatar_xid,
                       message_id=msg_id,
                       headers=json.dumps(headers),
                       payload=data.get('payload')
                       )
        resp.data = b'{"result": "ok", "message_id":"%s"}' % (msg_id,)
        resp.status = falcon.HTTP_200

logger.debug("Binding routes for Message module...")

_manager = MessageManager()

# routes
api.add_route("/{avatar_xid}/messages", MessageStore(_manager))
