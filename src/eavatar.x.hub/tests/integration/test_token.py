# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
from eavatar.hub.util import token


class JWTTest(unittest.TestCase):

    def test_token(self):
        key = "KepHDH38sKk7WX1x6X1zLbPvbRbFbUk1pWQdzDUrUqAYycVW"
        secret = "SXXgKA38a9dHvwXYxC3KnZ9jvbUZYVUKsE8rGiAvqp4p7fKx"
        xid = "AaBFgzmStr9yJBCjg4xpybCFnGaVboSeeuzh11xTM24BNH6G"


        data = dict(
            sub=xid,

        )
        tok = token.encode(data, secret)
        print(tok)
        decoded_data = token.decode(tok, key=key, verify=True)
        print(decoded_data)
        self.assertEqual(xid, decoded_data['sub'])