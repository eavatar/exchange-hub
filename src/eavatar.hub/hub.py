# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from gevent import monkey
monkey.patch_all()

import sys
import logging
import multiprocessing

#makes multiprocessing work when in freeze mode.
multiprocessing.freeze_support()

import socket
import time

# imports dependencies for PyInstaller to figure out what to include.
import depends
# prevent IDE regarding depends as not used.
depends.absolute_import

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',)


logger = logging.getLogger("main")


class Hub(object):

    def wait_for_cassandra(self):
        for i in range(30):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('cass1', 9042))
                return True
            except:
                logger.debug("Waiting for Cassandra...")
                time.sleep(1)
        return False

    def run(self):

        try:
            # works around the race condition
            if not self.wait_for_cassandra():
                logger.error("Cannot connect to Cassandra.")
                sys.exit(1)

            from eavatar.hub.main import Main

            main = Main()
            main.run()
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == '__main__':
    hub = Hub()
    hub.run()