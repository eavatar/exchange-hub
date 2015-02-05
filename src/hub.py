# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from gevent import monkey
monkey.patch_all()

import sys
import logging
import multiprocessing

#makes multiprocessing work when in freeze mode.
multiprocessing.freeze_support()
import pkg_resources


from eavatar.hub.main import Main

# imports dependencies for PyInstaller to figure out what to include.
import depends
# prevent IDE regarding depends as not used.
depends.absolute_import

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',)
try:
    main = Main()
    main.run()
except KeyboardInterrupt:
    sys.exit(0)