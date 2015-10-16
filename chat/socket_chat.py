#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: Implement websocket api
Author: 'yac'
Date: 
"""
import logging
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace


log = logging.getLogger('socketio')


@namespace('/chat')
class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    """ Implement API for websocket channels """

    user_list = []

    def initialize(self):
        """ Start websocket  """
        log.info("Chat session started")

    def on_file(self, msg):
        """ Broadcast file's for users and username
         :param msg: file
        """
        user = self.socket.session['nick']

        log.info('User <%s> sending <%s>', user, msg['imageName'])

        self.broadcast_event('user file', user, msg)
        return True

    def on_says(self, msg):
        """ Broadcast user's message and username
         :param msg: message text 
        """
        user = self.socket.session['nick']
        log.info('<%s> says: \'%s\'', user, msg)

        self.broadcast_event('receive msg', user, msg)
        return True

    def on_join(self, user):
        """ Broadcast connected user and number of user online """
        if not user:
            self.broadcast_event('user connected', '', ChatNamespace.user_list)
            return True

        log.info('User <%s> connected', user)

        ChatNamespace.user_list.append(user)

        self.socket.session['nick'] = user
        self.broadcast_event('user connected', user, ChatNamespace.user_list)

    def recv_disconnect(self):
        """ Broadcast disconnected user and send a 'disconnect' packet """
        if 'nick' in self.socket.session:
            log.info('User <%s> disconnected', self.socket.session['nick'])
            user = self.socket.session['nick']

            if user in ChatNamespace.user_list:
                ChatNamespace.user_list.remove(user)

            self.broadcast_event('user disconnected', user)
            self.disconnect(silent=True)
