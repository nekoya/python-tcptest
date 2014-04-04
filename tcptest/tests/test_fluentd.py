# -*- coding: utf-8 -*-

from nose.tools import assert_equal
import tcptest.fluentd
import fluent.event
import fluent.sender


class TestContext(object):
    def test_simple(self):
        with tcptest.fluentd.Server() as server:
            fluent.sender.setup('app', port=server.port)
            fluent.event.Event('follow', {'foo': 'bar'})
            fluent.event.Event('label', {'hoge': 'fuga'})
        assert_equal(
            server.logs,
            [
                ('app.follow:', {'foo': 'bar'}),
                ('app.label:', {'hoge': 'fuga'})
            ]
        )
