# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from ctypes import cdll

cdll.LoadLibrary('libsodium.so')
