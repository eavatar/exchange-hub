# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
from eavatar.hub.util import webutils
from eavatar.hub.sinks.base import SinkBase


class StaticFiles(SinkBase):

    def handle(self, req, resp, **kwargs):
        """
        Serves files from the static folder.
        """
        path = os.path.join(webutils.static_folder, req.path[8:])
        webutils.send_static_file(req, resp, path)
