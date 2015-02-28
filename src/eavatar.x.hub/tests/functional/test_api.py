# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json

import requests
from requests.auth import HTTPBasicAuth

from tests.functional.base import FunctionalTestCase
from cqlengine.management import sync_table, create_keyspace, delete_keyspace, drop_table
from eavatar.hub import avatar, message, anchor

from cqlengine import connection
from settings import KEYSPACE, DB_SERVERS
from eavatar.hub.util import token
from eavatar.hub.conf import NETWORK_KEY


JSON_CONTENT_TYPE = 'application/json; charset=utf-8'

HTTP_URL = 'http://127.0.0.1:5000'
HTTPS_URL = 'https://127.0.0.1:8443'


class ApiTest(FunctionalTestCase):
    alice_key = b"Kb7RAJFh1kmbW3CcdPN1n5TeX9DYN7pYAPy4fAkn4WDxUNh2"
    alice_secret = b"SXkFv96uDr3bbGNVrJUPaLt6gmxLzsxBwCzxmvjmadyFcutA"
    alice_xid = b"AWUPe1z13HBTHhPQCwJrR5FyhzCnNSXAzoZ7fyENvh7aruyr"

    bob_key = b"Kaw8YXpmyct3rm8tqeKkjyCc9AtaeyjP9PRR6VxbpecD1xXD"
    bob_secret = b"SXZD9hr1xjb8BTgqFFGsjJ557B279yBDYjxFHUC4c7fWEqsd"
    bob_xid = b"AWJ72FZ619HueRKgRCGbNxzwL1spfJS1yo1U7JSCgqVqQg6B"

    @classmethod
    def setUpClass(cls):
        connection.setup(DB_SERVERS, KEYSPACE)
        create_keyspace(KEYSPACE, replication_factor=1, strategy_class='SimpleStrategy')
        sync_table(avatar.Avatar)
        sync_table(anchor.Anchor)
        sync_table(message.Message)

#    @classmethod
#    def tearDownClass(cls):
#        connection.setup(DB_SERVERS, KEYSPACE)
#        delete_keyspace(KEYSPACE)

    def setUp(self):
        self.app = requests.Session()

    #### Root resource ####
    def test_get_root_resource(self):
        res = self.app.get(HTTP_URL + '/', headers={'accept': JSON_CONTENT_TYPE})

        self.assertEqual(200, res.status_code)

        # should return CORS header
        self.assertEquals(res.headers['Access-Control-Allow-Origin'], '*')

    def test_get_home_page(self):
        res = self.app.get(HTTP_URL + '/', headers={'accept': 'text/html'})
        self.assertEqual(200, res.status_code)
        self.assertTrue(b"EAvatar Technology Ltd" in res.text)

    def test_check_service_status(self):
        """
        The API should return OK on checking status.
        :return:
        """
        res = self.app.get(HTTP_URL + '/.status', headers={'accept': JSON_CONTENT_TYPE})
        self.assertEqual(200, res.status_code)
        self.assertTrue("ok" in res.text)

    def test_bearer_token_authentication_should_be_supported(self):
        url = "%s/self/anchors" % (HTTP_URL, )
        payload = dict(
            sub=self.alice_xid,
        )
        tok = token.encode(payload, self.alice_secret, NETWORK_KEY)
        bearer = b"Bearer %s" % tok
        res = self.app.get(url,
                           headers={b'accept': JSON_CONTENT_TYPE, b'Authorization': bearer})
        self.assertEqual(200, res.status_code)

    def test_empty_list_should_returned_when_no_anchor(self):
        """
        An empty list should be returned if no anchor found or the avatar doesn't exist.
        :return:
        """
        url = "%s/%s/anchors" % (HTTP_URL, self.alice_xid)
        res = self.app.get(url,
                           headers={'accept': JSON_CONTENT_TYPE},
                           auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.json())

    def test_anchor_crud(self):
        label1 = 'a'
        url = "%s/%s/anchors/%s" % (HTTP_URL, self.alice_xid, label1)
        anchor = {
            "label": label1,
            "value": "http://www.mocky.io/v2/54dc01b77d28597e102c6468"
        }

        data = json.dumps(anchor)

        res1 = self.app.put(url,
                            headers={'accept': JSON_CONTENT_TYPE, 'Content-Type': JSON_CONTENT_TYPE},
                            data=data,
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res1.status_code)

        res2 = self.app.get(url,
                            headers={'accept': JSON_CONTENT_TYPE},
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res2.status_code)
        jsonobj = res2.json()
        self.assertEqual("http://www.mocky.io/v2/54dc01b77d28597e102c6468", jsonobj["value"])

        anchor["value"] = "a_url"
        res3 = self.app.put(url,
                            headers={'accept': JSON_CONTENT_TYPE},
                            data=json.dumps(anchor),
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res3.status_code)

        res4 = self.app.delete(url,
                               headers={'accept': JSON_CONTENT_TYPE},
                               auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(204, res4.status_code)

    def test_create_new_avatar(self):
        data = {'xid': self.alice_xid}
        url = "%s/%s" % (HTTP_URL, self.alice_xid)
        res = self.app.put(url,
                           headers={'content-type': 'application/json'},
                           data=json.dumps(data),
                           auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res.status_code)
        json_res = res.json()
        self.assertEqual(json_res["result"], "ok")

    def test_can_get_self_messages(self):
        url = "%s/self/messages" % (HTTP_URL,)
        res = self.app.get(url,
                           headers={'content-type': 'application/json'},
                           auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))

        self.assertTrue(200, res.status_code)

    def test_can_send_message_to_avatar(self):
        data = {
            "headers": {
                "Content-type": "text/plain",
                "Content-length": 7,
            },
            "payload": "hello"
        }

        json_data = json.dumps(data)
        url = "%s/%s/messages" % (HTTP_URL, self.bob_xid)
        res = self.app.post(url,
                            headers={'content-type': 'application/json'},
                            data=json_data,
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(res.status_code, 200)
        res2 = self.app.get(url,
                            headers={'content-type': 'application/json'},
                            auth=HTTPBasicAuth(self.bob_xid, self.bob_secret))
        self.assertEqual(200, res2.status_code)
        data = res2.json()
        # print(data)
        self.assertTrue(len(data) > 0)

    def test_cannot_retrieve_others_messages(self):
        url = "%s/%s/messages" % (HTTP_URL, self.bob_xid)
        res = self.app.get(url,
                           headers={'content-type': 'application/json'},
                           auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(403, res.status_code)

    def test_can_send_message_to_self(self):
        data = {
            "headers": {
                "Content-type": "text/plain",
                "Content-length": 7,
            },
            "payload": "hello"
        }

        json_data = json.dumps(data)
        url = "%s/self/messages" % (HTTP_URL,)
        res = self.app.post(url,
                            headers={'content-type': 'application/json'},
                            data=json_data,
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(res.status_code, 200)
        data1 = res.json()
        # print("New msg ID: ", data1["message_id"])

        res2 = self.app.get(url,
                            headers={'content-type': 'application/json'},
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res.status_code)
        data2 = res2.json()
        # print(data2)
        self.assertTrue(len(data2) > 0)

