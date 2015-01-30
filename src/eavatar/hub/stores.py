# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Data stores.
The hub is stateless, all entities are stored in a store
"""

from abc import abstractmethod


class Store(object):

    @abstractmethod
    def save_avatar(self, avatar):
        pass

    @abstractmethod
    def load_avatar(self, xid):
        pass

    @abstractmethod
    def remove_avatar(self, xid):
        pass

    @abstractmethod
    def save_anchor(self, anchor):
        pass

    @abstractmethod
    def load_anchor(self, xid):
        pass

    @abstractmethod
    def remove_anchor(self, xid):
        pass


class MemoryStore(Store):
    """
    In-memory store for testing only.
    """
    def __init__(self):
        super(MemoryStore, self).__init__()
        self._avatars = {}
        self._anchors = {}

    def save_avatar(self, avatar):
        self._avatars[avatar["xid"]] = avatar

    def load_avatar(self, xid):
        return self._avatars.get(xid)

    def remove_avatar(self, xid):
        if xid in self._avatars.keys():
            del self._avatars[xid]


class LocalStore(Store):
    """
    The store for single node.
    """
    def __init__(self):
        super(LocalStore, self).__init__()


class CassandraStore(Store):
    """
    The store uses Cassandra as the database.
    """
    pass