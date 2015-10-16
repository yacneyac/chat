#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: 
Author: 'yac'
Date: 
"""

import os

from gevent import monkey
monkey.patch_all()
from django.core.wsgi import get_wsgi_application
from socketio.server import SocketIOServer
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")
app = get_wsgi_application()

if __name__ == '__main__':
    print('Listening on http://127.0.0.1:%s and on port 843 (flash policy server)\n'
          'press CTRL+C  for exit' % settings.PORT)

    SocketIOServer(('', settings.PORT), app,resource="socket.io", log_file='/tmp/access.log').serve_forever()