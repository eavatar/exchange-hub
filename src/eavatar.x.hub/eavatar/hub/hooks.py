# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Hooks run before or after requests.
"""

import binascii
import logging
import falcon
import six
from eavatar.hub.conf import AUTHENTICATION_HEADER, NETWORK_SECRET
from eavatar.hub.util import crypto, token

logger = logging.getLogger(__name__)


def _raise_unauthorized(title=b'Authentication required', desc=b'HTTP basic authentication scheme.'):
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

    auth_type = auth_type.lower()
    if auth_type == six.b('basic'):
        try:
            user_and_key = user_and_key.strip()
            user_and_key = binascii.a2b_base64(user_and_key)
            user_id, key = user_and_key.split(six.b(':'), 1)

            logger.debug("user_id: %s", user_id)

            if not crypto.validate_xid(user_id):
                _raise_unauthorized()

            xid = crypto.secret_key_to_xid(key)
            if xid != user_id:
                _raise_unauthorized()

            req.context['client_xid'] = user_id
            logger.debug("Client authenticated: %s", user_id)
            return
        except (binascii.Error, ValueError) as err:
            msg = ("Unable to determine user and pass/key encoding. "
                   "Got error: {0}").format(str(err))
            logger.debug(msg)
            _raise_unauthorized(desc=msg)

    elif auth_type == six.b("bearer"):
        try:
            tok = token.decode(user_and_key, NETWORK_SECRET, verify=True)
        except token.DecodeError:
            logger.debug("Token decode error", exc_info=True)
            tok = {}
            _raise_unauthorized()

        client_xid = tok.get("sub")
        if not client_xid:
            _raise_unauthorized(desc="Subject not specified in token.")

        if not crypto.validate_xid(client_xid):
            _raise_unauthorized()
        req.context['client_xid'] = client_xid
    else:
        _raise_unauthorized("Unsupported authentication method: %s" % auth_type)


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
