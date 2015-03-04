# -*- coding: utf-8 -*-

"""
Global Settings
"""


#### Cassandra datastore ####
KEYSPACE = 'exchange'
DB_SERVERS = ['cass1']
REPLICATION_FACTOR = 1
STRATEGY_CLASS = 'SimpleStrategy'

# Seconds to wait for Cassandra to start. must be integer.
CASSANDRA_STARTUP_TIME = 30


#### Web service ####
WEB_LISTEN_PORT = 5000
