# -*- coding: utf-8 -*-
"""
tcptest.memcached
~~~~~~~~~~~~~~~~~
"""

from . import TestServer


class Server(TestServer):
    """Memcached Test Server"""

    def build_command(self):
        return ('memcached', '-p', str(self.port))
