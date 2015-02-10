# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ujson as json

import falcon

from eavatar.hub.app import api

from tests.utils import FunctionalTest, FalconTestClient

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'


class ApiTest(FunctionalTest):
    alice_key = '8fSreudn6GdSiGPh6VDWBuTs7533dMNS2K4wdDBDaXuf'
    alice_secret = 'EpPFLbF85k73ZoTPMzG2hjJHD8y5WaCqvNzGM6GN7vtD'
    alice_address = 'QPndzFJTmycdfg5jxcSghX2scJnc3TNqVEfYtVTA5JVYiPQY'
    alice_auth = 'EAvatar sub="QPndzFJTmycdfg5jxcSghX2scJnc3TNqVEfYtVTA5JVYiPQY",sig="1234"'

    bob_key = 'HoTw7v3pvxLiDNAav3ziXR9ipLqkivP8MHbD9jUPsbT'
    bob_secret = 'GfKydnBomusuQAARppnbg44WbjuY3rAVuX5HBPEKHH6k'
    bob_address = 'QMJzoFDsv94hRBs9168ecZVTxxhuKAqGrE3PgkqpdxvpzWxP'
    bob_auth = 'EAvatar sub="QMJzoFDsv94hRBs9168ecZVTxxhuKAqGrE3PgkqpdxvpzWxP",sig="1234"'

    def setUp(self):
        self.app = FalconTestClient(api)

    #### Root resource ####
    def test_get_root_resource(self):
        res = self.app.get('/', headers={'accept': 'application/json'})

        self.assertEqual(falcon.HTTP_200, self.app.response.status)

    def test_get_home_page(self):
        res = self.app.get('/', headers={'accept': 'text/html'})
        self.assertEqual(falcon.HTTP_200, self.app.response.status)
        self.assertTrue(b"EAvatar Technology Ltd" in res[0])

    def test_check_service_status(self):
        """
        The API should return OK on checking status.
        :return:
        """
        res = self.app.get('/status', headers={'accept': 'application/json'})
        self.assertEqual(falcon.HTTP_200, self.app.response.status)
        self.assertTrue("OK" in res[0])

    ### keypair resource ###
    def test_generate_new_key_pair(self):
        res = self.app.post('/keypair', headers={'accept': JSON_CONTENT_TYPE})
        self.assertEqual(falcon.HTTP_200, self.app.response.status)
        result = json.loads(res[0])
        self.assertIsNotNone(result.get('xid'))
        self.assertIsNotNone(result.get('key'))
        self.assertIsNotNone(result.get('secret'))
