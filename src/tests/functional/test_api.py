# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ujson as json

import falcon

from eavatar.hub.app import api

from tests.utils import FunctionalTest, FalconTestClient

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'


class ApiTest(FunctionalTest):

    def setUp(self):
        self.app = FalconTestClient(api)

    #### Root resource ####
    def test_get_root_resource(self):
        res = self.app.get('/', headers={'accept': 'application/json'})

        self.assertEqual(falcon.HTTP_200, self.app.response.status)
