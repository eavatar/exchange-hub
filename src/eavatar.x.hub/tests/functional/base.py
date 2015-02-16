# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import requests
import gevent
from eavatar.hub.main import Main


class FunctionalTestCase(unittest.TestCase):
    """
    For integration tests with the agent.
    """
    _launcher = None

    @classmethod
    def setUpClass(cls):
        FunctionalTestCase._launcher = Main()
        server_greenlet = gevent.spawn(FunctionalTestCase._launcher.run)

    @classmethod
    def tearDownClass(cls):
        pass

