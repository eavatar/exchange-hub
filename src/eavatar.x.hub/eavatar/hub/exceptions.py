# -*- coding: utf-8 -*-
"""
Exceptions raised in eavtar.kits package.
"""
from __future__ import print_function, division, absolute_import


class EAvatarError(Exception):
    """
    Raised when error is framework-related but no specific error subclass exists.
    """
    def __init__(self, *args, **kwargs):
        super(EAvatarError, self).__init__(args, kwargs)


class DataError(EAvatarError):
    """
    Generic error related to database operations.
    """
    pass


class StoreExistsError(DataError):
    pass


class StoreNotFoundError(DataError):
    pass


class DataNotFoundError(DataError):
    """
    Raised to indicate the specified data item not found.
    """
    pass


class ReadonlyError(DataError):
    """
    Raised to indicate the cursor is in readonly mode when a mutating operation is invoked.
    """
    pass


class ConflictError(DataError):
    """
    Raised to indicate concurrent access issue such as trying to update an existing document with mismatched revision.
    """
    pass

