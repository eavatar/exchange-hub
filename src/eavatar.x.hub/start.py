# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Acts as the entry-point if the program is not started from the runtime.
"""

import sys
import logging

from cqlengine.management import sync_table, create_keyspace
from eavatar.hub import avatar, message, anchor

from cqlengine import connection
from settings import KEYSPACE, DB_SERVERS, REPLICATION_FACTOR, STRATEGY_CLASS


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',)
logger = logging.getLogger("main")


def setup():
    try:
        connection.setup(DB_SERVERS, KEYSPACE)
        create_keyspace(KEYSPACE,
                        replication_factor=REPLICATION_FACTOR,
                        strategy_class=STRATEGY_CLASS)
        sync_table(avatar.Avatar)
        sync_table(anchor.Anchor)
        sync_table(message.Message)
        sys.exit(0)
    except:
        sys.exit(1)


class Hub(object):

    def run(self):
        try:
            from eavatar.hub.main import Main

            main = Main()
            main.run()
        except KeyboardInterrupt:
            sys.exit(0)


def main():
    """
     Application entry-pont
    """
    hub = Hub()
    hub.run()


if __name__ == '__main__':
    main()