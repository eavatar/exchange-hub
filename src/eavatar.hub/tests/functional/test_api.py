# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ujson as json

import requests

from tests.functional.base import FunctionalTestCase

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'

HTTP_URL = 'http://127.0.0.1:8080'
HTTPS_URL = 'https://127.0.0.1:8443'


class ApiTest(FunctionalTestCase):
    alice_key = '8fSreudn6GdSiGPh6VDWBuTs7533dMNS2K4wdDBDaXuf'
    alice_secret = 'EpPFLbF85k73ZoTPMzG2hjJHD8y5WaCqvNzGM6GN7vtD'
    alice_address = 'QPndzFJTmycdfg5jxcSghX2scJnc3TNqVEfYtVTA5JVYiPQY'
    alice_auth = 'EAvatar sub="QPndzFJTmycdfg5jxcSghX2scJnc3TNqVEfYtVTA5JVYiPQY",sig="1234"'

    bob_key = 'HoTw7v3pvxLiDNAav3ziXR9ipLqkivP8MHbD9jUPsbT'
    bob_secret = 'GfKydnBomusuQAARppnbg44WbjuY3rAVuX5HBPEKHH6k'
    bob_address = 'QMJzoFDsv94hRBs9168ecZVTxxhuKAqGrE3PgkqpdxvpzWxP'
    bob_auth = 'EAvatar sub="QMJzoFDsv94hRBs9168ecZVTxxhuKAqGrE3PgkqpdxvpzWxP",sig="1234"'

    def setUp(self):
        self.app = requests

    #### Root resource ####
    def test_get_root_resource(self):
        res = self.app.get(HTTP_URL + '/', headers={'accept': JSON_CONTENT_TYPE})

        self.assertEqual(200, res.status_code)

    def test_get_home_page(self):
        res = self.app.get(HTTP_URL + '/', headers={'accept': 'text/html'})
        self.assertEqual(200, res.status_code)
        self.assertTrue(b"EAvatar Technology Ltd" in res.text)

    def test_check_service_status(self):
        """
        The API should return OK on checking status.
        :return:
        """
        res = self.app.get(HTTP_URL + '/status', headers={'accept': JSON_CONTENT_TYPE})
        self.assertEqual(200, res.status_code)
        self.assertTrue("OK" in res.text)

    ### keypair resource ###
    def test_generate_new_key_pair(self):
        res = self.app.post(HTTP_URL + '/keypair', headers={'accept': JSON_CONTENT_TYPE})
        self.assertEqual(200, res.status_code)
        result = res.json()
        xid = result.get('xid')
        key = result.get('key')
        secret = result.get('secret')
        #print("Secret key: ", secret)

        self.assertIsNotNone(xid)
        self.assertIsNotNone(key)
        self.assertIsNotNone(secret)
