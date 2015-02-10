# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import falcon
import falcon.testing
import gevent
from eavatar.hub.main import Main


class FunctionalTest(unittest.TestCase):
    """
    For integration tests with the agent.
    """
    _launcher = None

    @classmethod
    def setUpClass(cls):
        FunctionalTest._launcher = Main()
        server_greenlet = gevent.spawn(FunctionalTest._launcher.run)

    @classmethod
    def tearDownClass(cls):
        pass


class FalconTestClient(object):
    def __init__(self, app):
        self.app = app
        self.response = falcon.testing.StartResponseMock()

    def simulate_request(self, path, **kwargs):
        env = falcon.testing.create_environ(path=path, **kwargs)
        return self.app(env, self.response)

    def get(self, *args, **kwargs):
        kwargs['method'] = 'GET'
        return self.simulate_request(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs['method'] = 'PUT'
        return self.simulate_request(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs['method'] = 'POST'
        return self.simulate_request(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['method'] = 'DELETE'
        return self.simulate_request(*args, **kwargs)

    def head(self, *args, **kwargs):
        kwargs['method'] = 'HEAD'
        return self.simulate_request(*args, **kwargs)

    def patch(self, *args, **kwargs):
        kwargs['method'] = 'PATCH'
        return self.simulate_request(*args, **kwargs)

    def options(self, *args, **kwargs):
        kwargs['method'] = 'OPTIONS'
        return self.simulate_request(*args, **kwargs)

