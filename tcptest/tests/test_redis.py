#-*- coding: utf-8 -*-

from nose.tools import ok_, eq_, raises
import tcptest.redis

import redis


class TestContext(object):
    def test_simple(self):
        res = {}
        with tcptest.redis.Server(res=res) as server:
            db = redis.Redis(host='127.0.0.1', port=server.port, db=0)
            ok_(db.hset('hash', 'foo', 'bar'))
            ok_(db.hset('hash', 'hoge', 'fuga'))
            eq_(db.hgetall('hash'), {'foo': 'bar', 'hoge': 'fuga'})
        ok_(res['stdout'].endswith('bye bye...\n'))

    @raises(redis.ResponseError)
    def test_custom_conf(self):
        with tcptest.redis.Server(settings=dict(databases=4)) as server:
            db = redis.Redis(host='127.0.0.1',
                             port=server.port,
                             db=9)  # too large db number
            ok_(db.set('foo', 'bar'))
            ok_(db.get('foo'), 'bar')
