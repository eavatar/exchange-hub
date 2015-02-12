# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime
from cqlengine import columns
from cqlengine.models import Model


class Avatar(Model):
    """
    Represents anything with an identity that can send or receive messages.
    """
    xid = columns.Text(primary_key=True)
    owner_xid = columns.Text(default=None)  # the avatar who owns this one.
    parent_xid = columns.Text(default=None)  # the containment relationship.
    supervisor_xid = columns.Text(default=None)  # the avatar who can manage this one.
    kind = columns.Text(default='thing')
    created_at = columns.DateTime(default=datetime.utcnow())
    modified_at = columns.DateTime(default=datetime.utcnow())


class AvatarOwner(Model):
    """
    Represents relationship between an avatar and its owner.
    """
    owner_xid = columns.Text(primary_key=True)
    avatar_xid = columns.Text(primary_key=True, clustering_order="ASC")


class AvatarManager(object):
    model = Avatar

    def __init__(self):
        pass


class Anchor(Model):
    """
    Represents an outgoing link to an avatar or an endpoint.
    An anchor must belong to one and only one avatar.
    """
    avatar_xid = columns.Text(primary_key=True)
    label = columns.Text(primary_key=True, clustering_order="ASC", default='')
    kind = columns.Text(default="e")  # 'e' for endpoint, 'a' for avatar.
    value = columns.Text()  # an url if kind is endpoint, or an XID for avatar.


class Message(Model):
    """
    Represents messages received by an avatar. A message consists of:
    * a command
      Indicates if the message is a request or a response.
      For a response, 'ERR' is used for reporting error, 'RES' is to return successful result.
      Some commands from HTTP/1.1 are defined.
      - 'GET': The result of a GET request might be cached by the hub.
      - 'POST':
      - 'PUT':
      - 'DELETE':
      The URI part is designated as 'Destination' header.

    * a headers
      Contains metadata regarding the payload. Some well-known headers are:
      - 'Content-type': the content type of the payload, e.g. 'application/json'.
      - 'Content-length': the length in bytes of the payload
      - 'Destination': the resource intended to be the receiver on final target.
    * a payload(optional)
      The content to be sent as is. That is, the hub doesn't interpret or modify the payload.

    """
    avatar_xid = columns.Text(primary_key=True)
    message_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    command = columns.Text(default='POST')
    headers = columns.Text()
    payload = columns.Text(default=None)


class MessageManager(object):
    model = Message

    def __init__(self):
        pass