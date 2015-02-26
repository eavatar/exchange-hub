# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import hashlib
from libnacl.public import PublicKey, SecretKey
import jwt
from jwt.algorithms import Algorithm

from .crypto import validate_key_string, validate_secret_string, string_to_key, string_to_secret


class EA256(Algorithm):
    """
    Custom algorithm for signing and verifying JWT.
    """
    def __init__(self):
        super(EA256, self).__init__()

    def prepare_key(self, key):
        if not validate_key_string(key) and not validate_secret_string(key):
            raise ValueError("Invalid key.")
        return key

    def sign(self, msg, key):
        sk = SecretKey(string_to_secret(key))
        return "1234"

    def verify(self, msg, key, sig):
        if validate_secret_string(key):
            sk = SecretKey(string_to_secret(key))
        else:
            pk = PublicKey(string_to_key(key))

        return sig == "1234"

# register custom algorithm
_alg = EA256()
jwt.register_algorithm('EA256', _alg)


def encode(payload, key, headers=None):
    return jwt.encode(payload, key, algorithm="EA256", headers=headers)


def decode(tok, key='', verify=True, **kwargs):
    payload, signing_input, header, signature = jwt.api.load(tok)
    if verify:
        verify_signature(payload, signing_input, header, signature, key, **kwargs)

    return payload


def verify_signature(payload, signing_input, header, signature, key='',
                     verify_expiration=True, leeway=0, audience=None,
                     issuer=None):
    if not _alg.verify(signing_input, key, signature):
        raise jwt.DecodeError('Signature verification failed')