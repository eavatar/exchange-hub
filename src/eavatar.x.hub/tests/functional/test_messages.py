# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import requests
from requests.auth import HTTPBasicAuth
from .base import FunctionalTestCase


class MessagesTest(FunctionalTestCase):
    def setUp(self):
        self.app = requests.Session()

    def test_can_get_self_messages(self):
        url = "%s/self/messages" % (self.HTTP_URL,)
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
        url = "%s/%s/messages" % (self.HTTP_URL, self.bob_xid)
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
        url = "%s/%s/messages" % (self.HTTP_URL, self.bob_xid)
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
        url = "%s/self/messages" % (self.HTTP_URL,)
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

