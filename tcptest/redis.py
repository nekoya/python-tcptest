#-*- coding: utf-8 -*-
'''
tcptest.redis
~~~~~~~~~~~~~
'''

import tempfile
import time
import os

from . import TestServer


class Server(TestServer):
    '''Redis Test Server'''

    def __init__(self, settings=None, *args, **kw):
        super(Server, self).__init__(*args, **kw)
        self.settings = settings or {}

    def build_command(self):
        return ('redis-server', self.conffile)

    def _before_start(self):
        tmpdir = tempfile.gettempdir()
        now = int(time.time() * 1000)
        self.conffile = os.path.join(tmpdir, 'redis-%d.conf' % now)
        self.dbfile = os.path.join(tmpdir, 'redis-%d.rdb' % now)
        settings = {
            'port': self.port,
            'databases': 16,
            'dir': tmpdir,
            'dbfilename': self.dbfile,
        }
        settings.update(self.settings)
        with open(self.conffile, 'w+') as f:
            for (k, v) in settings.items():
                f.write('%s %s\n' % (k, v))

    def _after_stop(self):
        def rm(file):
            if os.path.exists(file):
                os.remove(file)
        rm(self.dbfile)
        rm(self.conffile)
