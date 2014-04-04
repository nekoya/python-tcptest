# -*- coding: utf-8 -*-
"""
tcptest.fluentd
~~~~~~~~~~~~~~~
"""

import json
import os
import tempfile
import time

from . import TestServer

config_template = """
<source>
  type forward
  port %(port)s
</source>

<match **>
  type stdout
</match>"""


class Server(TestServer):
    """fluentd test server"""

    def build_command(self):
        return ('fluentd', '-q', '-c', self.conffile.name)

    def _before_start(self):
        if self.res is None:
            self.res = {}
        self.conffile = tempfile.NamedTemporaryFile(delete=False)
        self.conffile.write(config_template % {'port': self.port})
        self.conffile.close()

    def _before_stop(self):
        time.sleep(0.01)  # wait fluentd log buffering

    def _after_stop(self):
        if os.path.exists(self.conffile.name):
            os.remove(self.conffile.name)

        self.logs = []
        for line in self.res['stdout'].rstrip('\n').split('\n'):
            elms = line.split(' ')
            self.logs.append((elms[3], json.loads(elms[4])))
