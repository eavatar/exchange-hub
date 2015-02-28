# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import logging
from eavatar.hub.conf import NETWORK_SECRET, NETWORK_XID, NETWORK_KEY
from eavatar.hub.util import token


logging.basicConfig(level="DEBUG")


class TokenTest(unittest.TestCase):

    def test_valid_token_should_pass(self):
        issuer_pk = b"KepHDH38sKk7WX1x6X1zLbPvbRbFbUk1pWQdzDUrUqAYycVW"
        issuer_sk = b"SXXgKA38a9dHvwXYxC3KnZ9jvbUZYVUKsE8rGiAvqp4p7fKx"
        issuer_xid = b"AaBFgzmStr9yJBCjg4xpybCFnGaVboSeeuzh11xTM24BNH6G"

        audience_pk = NETWORK_KEY
        audience_sk = NETWORK_SECRET

        data = dict(
            sub=issuer_xid,
        )
        tok = token.encode(data, issuer_sk, audience_pk)
        print(tok)
        decoded_data = token.decode(tok, audience_sk, verify=True)
        print(decoded_data)
        self.assertEqual(issuer_xid, decoded_data['sub'])