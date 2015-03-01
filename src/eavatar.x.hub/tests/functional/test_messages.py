# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import json
import requests
from requests.auth import HTTPBasicAuth
from tests.functional.base import FunctionalTestCase


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

    def test_can_dispatch_message(self):
        label1 = 'a'
        anchor_url = "%s/%s/anchors/%s" % (self.HTTP_URL, self.alice_xid, label1)
        anchor = {
            "label": label1,
            "value": "http://4c397230.ngrok.com/.status"
        }

        data = json.dumps(anchor)

        res1 = self.app.put(anchor_url,
                            headers={'accept': self.JSON_CONTENT_TYPE, 'Content-Type': self.JSON_CONTENT_TYPE},
                            data=data,
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res1.status_code)

        data = {
            "headers": {
                "Content-type": "text/plain",
                "Content-length": 7,
            },
            "payload": "hello"
        }

        msgdata = json.dumps(data)

        url = "%s/self/messages" % (self.HTTP_URL,)
        res = self.app.post(url,
                            headers={'content-type': 'application/json'},
                            data=msgdata,
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(res.status_code, 200)

        #res4 = self.app.delete(anchor_url,
        #                       headers={'accept': self.JSON_CONTENT_TYPE},
        #                       auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        #self.assertEqual(204, res4.status_code)