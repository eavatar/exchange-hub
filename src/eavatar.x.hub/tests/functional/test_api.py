# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json

import requests
from requests.auth import HTTPBasicAuth

from tests.functional.base import FunctionalTestCase

from eavatar.hub.util import token
from eavatar.hub.conf import NETWORK_KEY


class ApiTest(FunctionalTestCase):
    def setUp(self):
        self.app = requests.Session()

    #### Root resource ####
    def test_get_root_resource(self):
        res = self.app.get(self.HTTP_URL + '/', headers={'accept': self.JSON_CONTENT_TYPE})

        self.assertEqual(200, res.status_code)

        # should return CORS header
        self.assertEquals(res.headers['Access-Control-Allow-Origin'], '*')

    def test_get_home_page(self):
        res = self.app.get(self.HTTP_URL + '/', headers={'accept': 'text/html'})
        self.assertEqual(200, res.status_code)
        self.assertTrue(b"EAvatar Technology Ltd" in res.text)

    def test_check_service_status(self):
        """
        The API should return OK on checking status.
        :return:
        """
        res = self.app.get(self.HTTP_URL + '/.status', headers={'accept': self.JSON_CONTENT_TYPE})
        self.assertEqual(200, res.status_code)
        self.assertTrue("ok" in res.text)

    def test_bearer_token_authentication_should_be_supported(self):
        url = "%s/self/anchors" % (self.HTTP_URL, )
        payload = dict(
            sub=self.alice_xid,
        )
        tok = token.encode(payload, self.alice_secret, NETWORK_KEY)
        bearer = b"Bearer %s" % tok
        res = self.app.get(url,
                           headers={b'accept': self.JSON_CONTENT_TYPE, b'Authorization': bearer})
        self.assertEqual(200, res.status_code)

    def test_can_get_avatar_by_xid(self):
        url = "%s/%s" % (self.HTTP_URL, self.alice_xid)
        res = self.app.get(url,
                           headers={'accept': self.JSON_CONTENT_TYPE},
                           auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res.status_code)
        self.assertEqual(b"application/jrd+json", res.headers[b"Content-type"])
        json_res = res.json()
        self.assertEqual(url, json_res["subject"])

    def test_empty_list_should_returned_when_no_anchor(self):
        """
        An empty list should be returned if no anchor found or the avatar doesn't exist.
        :return:
        """
        url = "%s/%s/anchors" % (self.HTTP_URL, self.alice_xid)
        res = self.app.get(url,
                           headers={'accept': self.JSON_CONTENT_TYPE},
                           auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.json())

    def test_can_manage_own_anchors(self):
        label1 = 'a'
        url = "%s/%s/anchors/%s" % (self.HTTP_URL, self.alice_xid, label1)
        anchor = {
            "label": label1,
            "value": "http://www.mocky.io/v2/54dc01b77d28597e102c6468"
        }

        data = json.dumps(anchor)

        res1 = self.app.put(url,
                            headers={'accept': self.JSON_CONTENT_TYPE, 'Content-Type': self.JSON_CONTENT_TYPE},
                            data=data,
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res1.status_code)

        res2 = self.app.get(url,
                            headers={'accept': self.JSON_CONTENT_TYPE},
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res2.status_code)
        jsonobj = res2.json()
        self.assertEqual("http://www.mocky.io/v2/54dc01b77d28597e102c6468", jsonobj["value"])

        anchor["value"] = "a_url"
        res3 = self.app.put(url,
                            headers={'accept': self.JSON_CONTENT_TYPE},
                            data=json.dumps(anchor),
                            auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(200, res3.status_code)

        res4 = self.app.delete(url,
                               headers={'accept': self.JSON_CONTENT_TYPE},
                               auth=HTTPBasicAuth(self.alice_xid, self.alice_secret))
        self.assertEqual(204, res4.status_code)

