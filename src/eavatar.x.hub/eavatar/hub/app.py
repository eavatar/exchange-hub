# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
The application instance
"""

import falcon
import logging
from .middlewares import SetCorsHeader

logger = logging.getLogger(__name__)


def _generic_error_handler(ex, req, resp, params):
    """
    The catch-all error handler.

    :param ex:
    :param req:
    :param resp:
    :param params:
    :return:
    """
    logger.exception(ex)
    if isinstance(ex, falcon.HTTPError):
        raise ex
    raise falcon.HTTPInternalServerError(title="Internal Server Error",
                                         description="Error occurred")

# The API instance
set_cors_header = SetCorsHeader()
api = falcon.API(middleware=[set_cors_header])
api.add_error_handler(Exception, _generic_error_handler)


# shortcuts
def add_route(uri_template, resource):
    api.add_route(uri_template, resource)


def add_sink(sink, prefix="/"):
    api.add_sink(sink, prefix)