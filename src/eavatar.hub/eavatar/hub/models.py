# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cqlengine import columns
from cqlengine.models import Model


class Avatar(Model):
    id = columns.UUID(primary_key=True)
    first_name = columns.Text()
    last_name = columns.Text()