# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Hooks run before or after requests.
"""

import logging
import falcon
from eavatar.hub.conf import AUTHENTICATION_HEADER
from eavatar.hub.util import webutils, crypto

logger = logging.getLogger(__name__)


def _raise_unauthorized():
    raise falcon.HTTPUnauthorized(title='Authentication required',
                                  description='EAvatar needs specific authentication scheme.',
                                  scheme=AUTHENTICATION_HEADER)


def check_authorization(req, resp, params):
    if req.auth is None:
        _raise_unauthorized()

    auth = webutils.parse_authorization_header(req.auth)
    logger.debug("%r", auth)
    if auth['scheme'] != d.AUTHENTICATION_SCHEME:
        _raise_unauthorized()
    #logger.debug("Request type: %s", type(req))

    req.context['sub'] = auth['sub']


def check_owner(req, resp, params):
    """
    Check that the requester is the resource owner. Must run after check_avatar and check_authorization.

    :param req:
    :param resp:
    :param params:
    :return:
    """
    if req.context['sub'] != params['aid']:
        raise falcon.HTTPForbidden(title="Access Denied", description="Only owner can access.")


def check_avatar(req, resp, params):
    aid = params['aid']
    if not aid:
        raise falcon.HTTPNotFound()

    if not crypto.validate_xid(aid):
        raise falcon.HTTPNotFound()


def nocache(req, resp, params):
    resp.set_header(b'pragma', b'no-cache')
    resp.set_header(b'cache-control', b'no-cache')


def static_cacheable(req, resp):
    resp.set_header(b'cache-control', b'max-age=86400,s-maxage=86400')


def set_cors_header(req, resp):
    """
    Set response header for allowing access from any origins.

    :param req:
    :param resp:
    :return:
    """
    resp.set_header(b'Access-Control-Allow-Origin', '*')
