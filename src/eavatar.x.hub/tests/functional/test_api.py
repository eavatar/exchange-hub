# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json

import requests

from tests.functional.base import FunctionalTestCase

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'

HTTP_URL = 'http://127.0.0.1:5000'
HTTPS_URL = 'https://127.0.0.1:8443'


class ApiTest(FunctionalTestCase):
    alice_key = '8fSreudn6GdSiGPh6VDWBuTs7533dMNS2K4wdDBDaXuf'
    alice_secret = 'EpPFLbF85k73ZoTPMzG2hjJHD8y5WaCqvNzGM6GN7vtD'
    alice_xid = 'QPndzFJTmycdfg5jxcSghX2scJnc3TNqVEfYtVTA5JVYiPQY'
    alice_auth = 'EAvatar sub="QPndzFJTmycdfg5jxcSghX2scJnc3TNqVEfYtVTA5JVYiPQY",sig="1234"'

    bob_key = 'HoTw7v3pvxLiDNAav3ziXR9ipLqkivP8MHbD9jUPsbT'
    bob_secret = 'GfKydnBomusuQAARppnbg44WbjuY3rAVuX5HBPEKHH6k'
    bob_xid = 'QMJzoFDsv94hRBs9168ecZVTxxhuKAqGrE3PgkqpdxvpzWxP'
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

    def test_get_empty_anchor_list(self):
        """
        An empty list should be returned if no anchor found or the avatar doesn't exist.
        :return:
        """
        url = "%s/avatars/%s/anchors" % (HTTP_URL, self.alice_xid)
        res = self.app.get(url, headers={'accept': JSON_CONTENT_TYPE})
        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.json())

    def test_anchor_crud(self):
        label1 = 'a'
        url = "%s/avatars/%s/anchors/%s" % (HTTP_URL, self.alice_xid, label1)
        anchor = {
            "label": label1,
            "value": "http://www.mocky.io/v2/54dc01b77d28597e102c6468"
        }

        data = json.dumps(anchor)

        res1 = self.app.put(url, headers={'accept': JSON_CONTENT_TYPE, 'Content-Type': JSON_CONTENT_TYPE}, data=data)
        self.assertEqual(200, res1.status_code)

        res2 = self.app.get(url, headers={'accept': JSON_CONTENT_TYPE})
        self.assertEqual(200, res2.status_code)
        jsonobj = res2.json()
        self.assertEqual("http://www.mocky.io/v2/54dc01b77d28597e102c6468", jsonobj["value"])

        anchor["value"] = "a_url"
        res3 = self.app.put(url, headers={'accept': JSON_CONTENT_TYPE}, data=json.dumps(anchor))
        self.assertEqual(200, res3.status_code)

        res4 = self.app.delete(url, headers={'accept': JSON_CONTENT_TYPE})
        self.assertEqual(204, res4.status_code)




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

    def test_create_new_avatar(self):
        data = {'xid': self.alice_xid}
        res = self.app.put(HTTP_URL + '/avatars',
                           headers={'content-type': 'application/json'},
                           data=json.dumps(data))
        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertEqual(json_res["result"], "OK")

    def test_send_a_message_to_avatar(self):
        data = {
            "headers": {
                "Content-type": "text/plain",
                "Content-length": 7,
            },
            "payload": "hello"
        }

        json_data = json.dumps(data)

        res = self.app.post(HTTP_URL + '/route/' + self.alice_xid,
                            data=json_data)
        self.assertEqual(res.status_code, 200)