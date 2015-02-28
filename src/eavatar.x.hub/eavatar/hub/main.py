# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import sys
import time
import logging
import gevent
import socket
import settings
from gevent import pywsgi

from cqlengine import connection

from eavatar.hub.app import api

# order does matter for the imports
from eavatar.hub import (
    avatar,
    anchor,
    message,
    status,
    webfinger,
    webroot,
)


class Main(object):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._server = None

    def wait_for_cassandra(self):
        server_addr = settings.DB_SERVERS[0]
        parts = server_addr.split(":")
        server_addr = parts[0]
        port = 9042
        if len(parts) > 1:
            port = int(parts[1])

        self.logger.debug("Cassandra addr: %s, port: %s", server_addr, port)

        for i in range(settings.CASSANDRA_STARTUP_TIME):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((server_addr, port))
                return True
            except:
                self.logger.debug("Waiting for Cassandra...")
                time.sleep(1)
        return False

    def setup_cassandra_connection(self):
        self.logger.debug("Setting up Cassandra connection...")
        connection.setup(settings.DB_SERVERS, settings.KEYSPACE)

    def run(self):
        self.logger.debug("Starting hub node")
        if not self.wait_for_cassandra():
            self.logger.error("Cannot connect to Cassandra.")
            sys.exit(1)

        self.setup_cassandra_connection()

        self.logger.debug("Initializing web server...")
        self._server = pywsgi.WSGIServer(('', settings.WEB_LISTEN_PORT), api)
        self.logger.debug("Web server listen port: %d", settings.WEB_LISTEN_PORT)
        self.logger.debug("Starting web server...")
        self._server.serve_forever()
