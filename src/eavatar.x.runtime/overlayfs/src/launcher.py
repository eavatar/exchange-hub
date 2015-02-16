# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
The entry-point for the hub.
"""
from gevent import monkey
monkey.patch_all()

import multiprocessing

#makes multiprocessing work when in freeze mode.
multiprocessing.freeze_support()

import os
import sys
import logging
import importlib


ENV_ENTRYPOINT = "EAVATAR_ENTRYPOINT"
ENTRYPOINT = "start:main"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',)


def _mygetfilesystemencoding():
    old = sys.getfilesystemencoding

    def inner_func():
        ret = old()
        if ret is None:
            return 'UTF-8'
        else:
            return ret
    return inner_func


def patch_sys_getfilesystemencoding():
    # sys.getfilesystemencoding() always returns None when frozen on Ubuntu systems.
    patched_func = _mygetfilesystemencoding()
    sys.getfilesystemencoding = patched_func


def base_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        # assumes this file is located at src/eavatar/util/__init__.py
        abspath = os.path.abspath(os.path.join(__file__))
        abspath = os.path.dirname(abspath)
        return abspath


def add_code_path():
    """
    Add code folder to module path.
    :return:
    """
    sys.path.append(os.path.join(base_path(), 'code'))


def start():
    logger = logging.getLogger('app')
    patch_sys_getfilesystemencoding()

    add_code_path()

    # imports dependencies for PyInstaller to figure out what to include.
    import depends
    # prevent IDE regarding depends as not used.
    depends.absolute_import

    entrypoint = os.environ.get(ENV_ENTRYPOINT, ENTRYPOINT)

    (mod_path, func) = entrypoint.split(":")

    try:
        logger.info("Importing entry point at %s", entrypoint)
        mod_main = importlib.import_module(mod_path)
        main_func = getattr(mod_main, func)
    except ImportError:
        logger.error("Failed to import entry-point module.", exc_info=True)
        sys.exit(-1)
    except AttributeError:
        logger.error("No entry-point found.", exc_info=True)
        sys.exit(-1)

    try:
        main_func()
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.error("Error in entry point", exc_info=True)


# Start if run as entry point
if __name__ == '__main__':
    start()