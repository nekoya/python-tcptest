# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_, raises
import tcptest.redis

import redis
import time


class TestContext(object):
    def test_simple(self):
        res = {}
        with tcptest.redis.Server(res=res) as server:
            db = redis.Redis(host='127.0.0.1', port=server.port, db=0)
            ok_(db.hset('hash', 'foo', 'bar'))
            ok_(db.hset('hash', 'hoge', 'fuga'))
            eq_(db.hgetall('hash'), {b'foo': b'bar', b'hoge': b'fuga'})
        ok_(res['stdout'].endswith(b'bye bye...\n'))

    @raises(redis.ResponseError)
    def test_custom_conf(self):
        with tcptest.redis.Server(settings=dict(databases=4)) as server:
            db = redis.Redis(host='127.0.0.1',
                             port=server.port,
                             db=9)  # too large db number
            ok_(db.set('foo', 'bar'))
            ok_(db.get('foo'), 'bar')

    def test_invalid_conf(self):
        server = tcptest.redis.Server(settings={'host':'127.0.0.1', 'invalidparam':'123456'})
        try:
            server.start()
        except Exception as e:
            ok_(e.args[0]['stderr'].endswith('Bad directive or wrong number of arguments\n'))


class TestReplication(object):
    def setup(self):
        self.master = tcptest.redis.Server()
        self.master.start()

        slave_settings = {'slaveof': 'localhost %d' % self.master.port}
        self.slave = tcptest.redis.Server(settings=slave_settings)
        self.slave.start()

    def teardown(self):
        self.slave.stop()
        self.master.stop()

    def test_replication(self):
        master = redis.Redis(host='127.0.0.1', port=self.master.port, db=0)
        slave = redis.Redis(host='127.0.0.1', port=self.slave.port, db=0)

        # wait replication link
        max = 40
        for i in range(max):
            time.sleep(0.01)
            if slave.info()['master_link_status'] == 'up':
                break
        if i + 1 == max:
            raise Exception('slave does not work well')

        eq_(master.info()['connected_slaves'], 1)
        info_slave0 = master.info()['slave0']
        if isinstance(info_slave0, dict):
            eq_(info_slave0['ip'], '::1')
            eq_(info_slave0['state'], 'online')
            eq_(info_slave0['port'], self.slave.port)
        else:
            eq_(info_slave0, '127.0.0.1,%d,online' % self.slave.port)

        eq_(slave.info()['master_port'], self.master.port)
        eq_(slave.info()['role'], 'slave')
        eq_(slave.info()['master_link_status'], 'up')

        ok_(master.set('foo', 'bar'))
        eq_(master.get('foo'), b'bar')
        eq_(slave.get('foo'), b'bar')
