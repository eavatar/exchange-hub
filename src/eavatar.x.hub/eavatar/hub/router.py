# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import json
import logging
import falcon

from datetime import datetime
from cqlengine import TimeUUID
from eavatar.hub.app import api

from eavatar.hub import views
from eavatar.hub import message

logger = logging.getLogger(__name__)


class RouterResource(views.ResourceBase):
    def on_post(self, req, resp, address=""):
        """
        Routes a message to its destination.

        :param req:
        :param resp:
        :return:
        """
        msg_data = json.load(req.stream)
        msg_id = str(TimeUUID.from_datetime(datetime.utcnow()))
        msg_data['headers']['destination'] = address
        msg_data['headers']['msgid'] = msg_id

        msg = message.Message(avatar_xid=address,
                              message_id=msg_id,
                              headers=json.dumps(msg_data['headers']),
                              payload=json.dumps(msg_data['payload']))
        msg.save()
        resp.status = falcon.HTTP_200


logger.debug("Binding routes for Router module...")
# routes
api.add_route("/route/{address}", RouterResource())

