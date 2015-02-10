#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""

"""

from cqlengine.management import sync_table
from eavatar.hub.models import Avatar

sync_table(Avatar)


