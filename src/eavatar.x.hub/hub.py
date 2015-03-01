# -*- coding: utf-8 -*-
"""
Acts as the entry-point if the program is not started from the runtime.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys
import logging
from gevent import monkey
monkey.patch_all()


def main():
    """
     Application entry-point
    """
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format,)
    logger = logging.getLogger("main")

    try:
        from eavatar.hub.main import Main

        launcher = Main()
        launcher.run()
    except KeyboardInterrupt:
        logger.debug("Stopping Hub")
        sys.exit(0)


if __name__ == '__main__':
    main()
