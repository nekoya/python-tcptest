# -*- coding: utf-8 -*-
"""
tcptest.redis
~~~~~~~~~~~~~
"""

import tempfile
import time
import os

from . import TestServer


class Server(TestServer):
    """Redis Test Server"""

    def __init__(self, settings=None, *args, **kw):
        super(Server, self).__init__(*args, **kw)
        self.settings = settings or {}

    def build_command(self):
        args = ['redis-server']
        for (k, v) in self.settings.items():
            args.append('--%s' % k)
            args.extend(str(v).split(' '))
        return tuple(args)

    def _before_start(self):
        self.settings['port'] = self.port

        if 'databases' not in self.settings:
            self.settings['databases'] = 16

        if 'dir' not in self.settings:
            self.settings['dir'] = tempfile.gettempdir()

        if 'dbfilename' not in self.settings:
            now = int(time.time() * 1000)
            self.settings['dbfilename'] = 'redis-%d.rdb' % now

    def _after_stop(self):
        dbfilename = os.path.join(self.settings['dir'],
                                  self.settings['dbfilename'])
        if os.path.exists(dbfilename):
            os.remove(dbfilename)
