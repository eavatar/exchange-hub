# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

### Authentication ####

# the scheme for authenticating clients.
AUTHENTICATION_SCHEME = 'Basic'

# return to client to
AUTHENTICATION_HEADER = 'Basic realm="eavatar.com"'

# the base58-encoded secret key for joining the overlay network.
NETWORK_SECRET = 'EHyEbr77n9CXYrSMyQ8SzqArFyTALc8wyb4KXbwV3LXq'

VERSION_STRING = "0.1.0"


MAX_MESSAGE_SIZE = 1024
MAX_REQUEST_SIZE = 4096


##### Environment variable ####
ENV_HUB_HOME = 'HUB_HOME'
ENV_HUB_SECRET_KEY = 'HUB_SECRET_KEY'


# overrides with user settings
from settings import *

