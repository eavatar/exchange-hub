# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


VERSION_STRING = "0.1.0"

### Authentication ####

# the scheme for authenticating clients.
AUTHENTICATION_SCHEME = b'Basic'

# the base58-encoded keys for the EAvatar network.
NETWORK_SECRET = b"6cQaJceBk3HxyzwV7efMhHEGDm1JfbLtW3wwc3t5X56s"
NETWORK_KEY = b"H1QX5k1yuDffJEDAkJJi5frh4AUbkiQRWTPpBnGe3tua"
NETWORK_XID = b"QSbCHL9ehEAWj58Z7juTXgNawyQgEwY4naVu9bEEaetwwKgq"

# the secret for pre-encrypting JWTs.
TOKEN_SECRET = b"avatoken"


MAX_MESSAGE_SIZE = 1024
MAX_REQUEST_SIZE = 4096


##### Environment variable ####
ENV_HUB_HOME = 'HUB_HOME'
ENV_HUB_SECRET_KEY = 'HUB_SECRET_KEY'

# overrides with user settings
from settings import *


# return to client to provide the network's XID, from which the public key can be retrieved.
AUTHENTICATION_HEADER = b'Bearer realm="eavatar.net",xid="%s"' % (NETWORK_XID,)

