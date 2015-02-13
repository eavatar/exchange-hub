# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import argparse
from cqlengine.management import sync_table, create_keyspace, delete_keyspace, drop_table
from eavatar.hub import avatar, message, anchor

from cqlengine import connection
from settings import KEYSPACE, DB_SERVERS


class HubCLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Command-line tool for EAvatar Hub',
            usage='''hubcli <command> [<args>]

The most commonly used commands are:
   sync_tables      Synchronize models with Cassandra
   create_space     Create the key space for the hub
   remove_space     Delete the key space used by the hub

''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def sync_tables(self):
        parser = argparse.ArgumentParser(
            description='Synchronize models with Cassandra')
        args = parser.parse_args(sys.argv[2:])

        connection.setup(DB_SERVERS, KEYSPACE)
        sync_table(avatar.Avatar)
        sync_table(anchor.Anchor)
        sync_table(message.Message)

    def drop_tables(self):
        parser = argparse.ArgumentParser(
            description='Delete tables for models')
        args = parser.parse_args(sys.argv[2:])

        connection.setup(DB_SERVERS, KEYSPACE)
        drop_table(avatar.Avatar)
        drop_table(anchor.Anchor)
        drop_table(message.Message)

    def create_space(self):
        parser = argparse.ArgumentParser(
            description='Create the key space for the hub')
        args = parser.parse_args(sys.argv[2:])

        connection.setup(DB_SERVERS, KEYSPACE)
        create_keyspace(KEYSPACE, replication_factor=1, strategy_class='SimpleStrategy')

    def remove_space(self):
        parser = argparse.ArgumentParser(
            description='Delete the key space used by the hub')
        args = parser.parse_args(sys.argv[2:])
        connection.setup(DB_SERVERS, KEYSPACE)
        delete_keyspace(KEYSPACE)


def main():
    HubCLI()

if __name__ == '__main__':
    main()