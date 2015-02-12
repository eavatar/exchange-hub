# -*- coding: utf-8 -*-

"""
Global Settings
"""

#### Authentication ####

# the scheme for authenticating clients.
AUTHENTICATION_SCHEME = 'eavatar'

# return to client to
AUTHENTICATION_HEADER = 'EAvatar realm="eavatar.com",key="abcd"'

# the base58-encoded secret key for joining the overlay network.
NETWORK_SECRET = 'EHyEbr77n9CXYrSMyQ8SzqArFyTALc8wyb4KXbwV3LXq'

VERSION_STRING = "0.1.0"

# return as the root resource.
AGENT_INFO = {
            "EAvatar": "A versatile agent.",
            "version": VERSION_STRING,
            "vendor": {
                "name": "EAvatar Technology Ltd.",
                "version": "0.1.0"
            },
}


# The ID for built-in message listener.
MESSAGE_LISTENER_ID = 'message'

MAX_MESSAGE_SIZE = 1024
MAX_REQUEST_SIZE = 4096


##### Environment variable ####
AVA_HOME = 'AVA_HOME'
AVA_SECRET_KEY = 'AVA_SECRET_KEY'


#### Cassandra datastore ####
KEYSPACE = 'exchange'
DB_SERVERS = ['cass1']

