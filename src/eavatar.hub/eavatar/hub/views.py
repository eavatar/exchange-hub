# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging
import falcon
import base58

from datetime import datetime
from cqlengine import connection
from cqlengine import TimeUUID
from eavatar.hub import util
from eavatar.hub import hooks
from eavatar.hub import models
from settings import KEYSPACE, DB_SERVERS

logger = logging.getLogger(__name__)

ENCODING = 'utf-8'

RESULT_OK = '{"result": "OK"}'
EMPTY_LIST = '[]'


class ResourceBase(object):
    def __init__(self, context=None):
        self._context = context
        connection.setup(DB_SERVERS, KEYSPACE)

    @staticmethod
    def validate_content_is_json(req):
        if req.content_type is None or (not req.content_type.startswith('application/json')):
            raise falcon.HTTPUnsupportedMediaType(description='Accept JSON format only.')

    @staticmethod
    def validate_request_size(req, limit):
        if not req.content_length or req.content_length > limit:
            raise falcon.HTTPBadRequest(title='Bad Request', description='Request exceeded size limit.')



    @staticmethod
    def get_user(req):
        return req.context['sub']


class StatusResource(ResourceBase):
    """
    Check the service status.
    """
    def on_get(self, req, resp):
        resp.body = RESULT_OK
        resp.status = falcon.HTTP_200


class AvatarCollection(ResourceBase):
    def on_get(self, req, resp):
        resp.body = EMPTY_LIST
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp):
        try:
            data = json.load(req.stream, encoding=ENCODING)
            avatar = models.Avatar(xid=data.get('xid'), kind=data.get('kind'))
            avatar.save()
            resp.body = RESULT_OK
            resp.status = falcon.HTTP_200
        except:
            raise


class AvatarResource(ResourceBase):

    def on_get(self, req, resp, avatar_xid):
        rs = models.Avatar.objects(xid=avatar_xid).limit(1)
        if len(rs) == 0:
            raise falcon.HTTPNotFound

        resp.body = json.dumps(rs[0])
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, avatar_xid):
        pass


class KeypairResource(ResourceBase):

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


class MessageStore(ResourceBase):

    def on_get(self, req, resp, avatar_xid):
        """
        Gets last N messages of the specified avatar.

        :param req:
        :param resp:
        :param avatar_xid: the avatar's XID.
        :return:
        """
        qs = models.Message.objects(avatar_xid=avatar_xid).limit(10)
        result = []
        for m in qs:
            result.append(m)

        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

class RouterResource(ResourceBase):
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
        msg = models.Message(avatar_xid=address,
                             message_id=msg_id,
                             command=msg_data['command'],
                             headers=msg_data['headers'],
                             payload=msg_data['payload'])
        msg.save()
        resp.status = falcon.HTTP_200


class RootResource(ResourceBase):
    def on_head(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        logger.debug(req.get_header(b'accept'))
        prefered_type = req.client_prefers([b'text/html', b'application/json'])
        if prefered_type == b'application/json':
            resp.status = falcon.HTTP_200
            resp.body = b'{"message": "Hello from root!"}'
        else:
            util.webutils.send_static_file(req, resp, 'index.html', media_type=b'text/html; charset=utf-8')


@falcon.after(hooks.static_cacheable)
class FaviconResource(object):
    def __init__(self, *args, **kwargs):
        super(FaviconResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        util.webutils.send_static_file(req, resp, 'favicon.ico', media_type=b'image/vnd.microsoft.icon')


