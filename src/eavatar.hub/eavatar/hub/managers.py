# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Model managers providing extra business logic if needed.
"""


from eavatar.hub import models


class BaseManager(object):
    def __init__(self, model):
        self.model = model
        super(BaseManager, self).__init__()

    def load(self, xid):
        return self.model.objects(xid=xid).first()

    def save(self, avatar):
        avatar.save()

    def remove(self, xid):
        self.model.objects(xid=xid).delete()

    def remove_all(self):
        self.model.objects.all().delete()

    def find(self, q):
        return self.model.objects(q)

    def find_all(self, limit=1000):
        return self.model.objects.all().limit(limit)

    def find_one(self, q):
        return self.model.objects(q).first()


