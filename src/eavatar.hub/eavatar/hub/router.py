# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import json
import falcon

from datetime import datetime
from cqlengine import TimeUUID
from eavatar.hub import views
from eavatar.hub import message


class RouterResource(views.ResourceBase):
    def on_post(self, req, resp, address=""):
        """
        Routes a message to its destination.

        :param req:
        :param resp:
        :return:
        """
        msg_data = json.dumps(req.stream)
        msg_id = TimeUUID.from_datetime(datetime.utcnow())
        msg_data['headers']['destination'] = address
        msg_data['headers']['msgid'] = msg_id
        msg = message.Message(avatar_xid=address,
                             message_id=msg_id,
                             command=msg_data['command'],
                             headers=msg_data['headers'],
                             payload=msg_data['payload'])
        msg.save()
        resp.status = falcon.HTTP_200

