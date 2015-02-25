# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import six


class SetCorsHeader(object):
    def process_request(self, req, resp):
        """Set CORS header.

        Args:
            req: Request object.
            resp: Response object.
        """
        resp.set_header(b'Access-Control-Allow-Origin', b'*')
