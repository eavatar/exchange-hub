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


