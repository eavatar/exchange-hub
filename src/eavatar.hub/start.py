# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Acts as the entry-point if the program is not started from the runtime.
"""

import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',)


logger = logging.getLogger("main")


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