# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import requests
import gevent
from cqlengine import connection
from cqlengine.management import sync_table, create_keyspace, delete_keyspace, drop_table

from eavatar.hub.main import Main
from settings import KEYSPACE, DB_SERVERS
from eavatar.hub import avatar, message, anchor


class FunctionalTestCase(unittest.TestCase):
    """
    For integration tests with the agent.
    """
    _launcher = None

    alice_key = b"Kb7RAJFh1kmbW3CcdPN1n5TeX9DYN7pYAPy4fAkn4WDxUNh2"
    alice_secret = b"SXkFv96uDr3bbGNVrJUPaLt6gmxLzsxBwCzxmvjmadyFcutA"
    alice_xid = b"AWUPe1z13HBTHhPQCwJrR5FyhzCnNSXAzoZ7fyENvh7aruyr"

    bob_key = b"Kaw8YXpmyct3rm8tqeKkjyCc9AtaeyjP9PRR6VxbpecD1xXD"
    bob_secret = b"SXZD9hr1xjb8BTgqFFGsjJ557B279yBDYjxFHUC4c7fWEqsd"
    bob_xid = b"AWJ72FZ619HueRKgRCGbNxzwL1spfJS1yo1U7JSCgqVqQg6B"

    JSON_CONTENT_TYPE = 'application/json; charset=utf-8'
    JRD_CONTENT_TYPE = 'application/jrd+json'

    #HTTP_URL = 'http://127.0.0.1:8080'
    HTTP_URL = "http://x-test.eavatar.net"
    HTTPS_URL = 'https://127.0.0.1:8443'

    @classmethod
    def setUpClass(cls):
        FunctionalTestCase._launcher = Main()
        server_greenlet = gevent.spawn(FunctionalTestCase._launcher.run)
        connection.setup(DB_SERVERS, KEYSPACE)
        create_keyspace(KEYSPACE, replication_factor=1, strategy_class='SimpleStrategy')
        sync_table(avatar.Avatar)
        sync_table(anchor.Anchor)
        sync_table(message.Message)

    @classmethod
    def tearDownClass(cls):
        pass

