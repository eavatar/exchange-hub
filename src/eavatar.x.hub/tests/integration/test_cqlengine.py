# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import unittest

from cqlengine import connection
from cqlengine.management import sync_table, create_keyspace, delete_keyspace

KEYSPACE = b"exchange_test"

from eavatar.hub import avatar, anchor, message


class CQLEngineTest(unittest.TestCase):

    def setUp(self):
        connection.setup(['127.0.0.1'], KEYSPACE)
        create_keyspace(KEYSPACE, replication_factor=1, strategy_class='SimpleStrategy')
        sync_table(avatar.Avatar)
        sync_table(anchor.Anchor)
        sync_table(message.Message)

    def tearDown(self):
        delete_keyspace(KEYSPACE)

    def test_create_example_model(self):
        em1 = avatar.Avatar.create(xid='1234')
        self.assertTrue(avatar.Avatar.objects.count() == 1)