# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Hooks run before or after requests.
"""

import binascii
import logging
import falcon
import six
from eavatar.hub.conf import AUTHENTICATION_HEADER, AUTHENTICATION_SCHEME
from eavatar.hub.util import webutils, crypto

logger = logging.getLogger(__name__)


def _raise_unauthorized(title='Authentication required', desc='HTTP basic authentication scheme.'):
    raise falcon.HTTPUnauthorized(title=title,
                                  description=desc,
                                  scheme=AUTHENTICATION_HEADER)


def check_authentication(req, resp, resource, params):
    logger.debug("Checking authentication...")

    http_auth = req.auth

    if http_auth is None:
        msg = "No authentication header value is given."
        _raise_unauthorized(desc=msg)

    if isinstance(http_auth, six.string_types):
            http_auth = http_auth.encode('ascii')

    auth_type = ""
    user_and_key = ""

    try:
        auth_type, user_and_key = http_auth.split(six.b(' '), 1)
    except ValueError as err:
        msg = ("Basic authorize header value not properly formed. "
               "Supplied header {0}. Got error: {1}")
        msg = msg.format(http_auth, str(err))
        logger.debug(msg)
        _raise_unauthorized(desc=msg)

    if auth_type.lower() == six.b('basic'):
        try:
            user_and_key = user_and_key.strip()
            user_and_key = binascii.a2b_base64(user_and_key)
            user_id, key = user_and_key.split(six.b(':'), 1)
            # TODO: verify key here
            req.context['client_xid'] = user_id
            logger.debug("Client authenticated: %s", user_id)
            return
        except (binascii.Error, ValueError) as err:
            msg = ("Unable to determine user and pass/key encoding. "
                   "Got error: {0}").format(str(err))
            logger.debug(msg)
            _raise_unauthorized(desc=msg)

    _raise_unauthorized()


def check_owner(req, resp, resource, params):
    """
    Check that the requester is the resource owner. Must run after check_avatar and check_authorization.

    :param req:
    :param resp:
    :param params:
    :return:
    """
    if req.context['client_xid'] != params['avatar_xid']:
        raise falcon.HTTPForbidden(title="Access Denied", description="Only owner can access.")


def check_avatar(req, resp, resource, params):
    aid = params['avatar_xid']
    if not aid:
        raise falcon.HTTPNotFound()

    if not crypto.validate_xid(aid):
        raise falcon.HTTPNotFound()


def nocache(req, resp, resource, params):
    resp.set_header(b'pragma', b'no-cache')
    resp.set_header(b'cache-control', b'no-cache')


def static_cacheable(req, resp, resource, params):
    resp.set_header(six.b('cache-control'), six.b('max-age=86400,s-maxage=86400'))


def set_cors_header(req, resp, resource, params):
    """
    Set response header for allowing access from any origins.

    :param req:
    :param resp:
    :return:
    """
    resp.set_header(b'Access-Control-Allow-Origin', six.b('*'))
