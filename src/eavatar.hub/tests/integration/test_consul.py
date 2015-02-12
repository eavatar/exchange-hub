# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import unittest
import consul


class ConsulTest(unittest.TestCase):

    def setUp(self):
        self.c = consul.Consul()

    def test_catalog_nodes(self):
        self.assertTrue(len(self.c.catalog.nodes()) > 0)