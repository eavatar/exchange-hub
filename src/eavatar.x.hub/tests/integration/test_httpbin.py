# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import unittest
import requests


class HttpbinTest(unittest.TestCase):

    def test_http_post(self):
        data = '{"result: "OK"}'
        r = requests.post('http://httpbin.org/post', data=data)
        self.assertTrue(200, r.status_code)
        result = r.json()
        #print(result['data'])
        self.assertEqual(data, result['data'])

    def test_http_response_mock(self):
        data = '{"result: "OK"}'
        r = requests.post('http://www.mocky.io/v2/54dc01b77d28597e102c6468', data=data)
        self.assertTrue(200, r.status_code)
        result = r.json()
        self.assertEqual("OK", result['result'])
