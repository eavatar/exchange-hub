# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import requests
from .base import FunctionalTestCase


class WebFingerTest(FunctionalTestCase):
    def setUp(self):
        self.app = requests.Session()

    def test_can_check_avatar_via_webfinger_anonymously(self):
        resource = "%s" % self.alice_xid
        url = "%s/.wellknown/webfinger?resource=%s" % (self.HTTP_URL, resource)
        res = self.app.head(url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.alice_xid, res.headers["x-avatar"])

    def test_can_query_avatar_via_webfinger_anonymously(self):
        resource = "%s" % self.alice_xid
        url = "%s/.wellknown/webfinger?resource=%s" % (self.HTTP_URL, resource)
        res = self.app.get(url, headers={'accept': self.JRD_CONTENT_TYPE})
        self.assertEqual(200, res.status_code)
        self.assertEqual(self.alice_xid, res.headers["x-avatar"])
        self.assertEqual(self.JRD_CONTENT_TYPE, res.headers[b"Content-type"])
        json_res = res.json()
        self.assertEqual(resource, json_res["subject"])
