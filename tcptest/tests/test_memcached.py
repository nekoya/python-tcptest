# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_
import tcptest.memcached

import memcache


class TestContext(object):
    def test_server(self):
        res = {}
        with tcptest.memcached.Server(res=res) as server:
            port = server.port
            ok_(isinstance(port, int))
            ok_(not isinstance(port, bool))

            memd = memcache.Client(['127.0.0.1:%d' % port])
            eq_(memd.get('foo'), None)
            ok_(memd.set('foo', 'bar'))
            eq_(memd.get('foo'), 'bar')
        eq_(sorted(res.keys()), ['stderr', 'stdout'])
        eq_(memd.get('foo'), None)  # stopped


class TestStartStop(object):
    def setup(self):
        self.server = tcptest.memcached.Server()
        self.server.start()

    def teardown(self):
        self.server.stop()

    def test_server(self):
        memd = memcache.Client(['127.0.0.1:%d' % self.server.port])
        eq_(memd.get('foo'), None)
        ok_(memd.set('foo', 'baz'))
        eq_(memd.get('foo'), 'baz')
