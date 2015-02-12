# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import unittest

from cqlengine import connection
from cqlengine.management import sync_table, create_keyspace, delete_keyspace

KEYSPACE = b"exchange_test"

from eavatar.hub.models import Avatar, Anchor, Message


class CQLEngineTest(unittest.TestCase):

    def setUp(self):
        connection.setup(['127.0.0.1'], KEYSPACE)
        create_keyspace(KEYSPACE, replication_factor=1, strategy_class='SimpleStrategy')
        sync_table(Avatar)
        sync_table(Anchor)
        sync_table(Message)

    def tearDown(self):
        delete_keyspace(KEYSPACE)

    def test_create_example_model(self):
        em1 = Avatar.create(xid='1234')
        self.assertTrue(Avatar.objects.count() == 1)