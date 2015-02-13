# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Anchor management.
"""

from cqlengine import columns
from cqlengine.models import Model

from eavatar.hub.managers import BaseManager


class Anchor(Model):
    """
    Represents an outgoing link to an avatar or an endpoint.
    An anchor must belong to one and only one avatar.
    """
    avatar_xid = columns.Text(primary_key=True, partition_key=True)
    label = columns.Text(primary_key=True, clustering_order="ASC", default='')
    kind = columns.Text(default="e")  # 'e' for endpoint, 'a' for avatar.
    value = columns.Text()  # an url if kind is endpoint, or an XID for avatar.


class AnchorManager(BaseManager):
    model = Anchor

    def __init__(self):
        super(Anchor, self).__init(Anchor)