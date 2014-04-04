# -*- coding: utf-8 -*-

from nose.tools import ok_, eq_, assert_raises
import tcptest
import tcptest.memcached

import socket


def test_empty_port():
    p1 = tcptest.empty_port()
    p2 = tcptest.empty_port()
    ok_(isinstance(p1, int))
    ok_(isinstance(p2, int))
    ok_(not isinstance(p1, bool))
    ok_(not isinstance(p2, bool))
    ok_(p1 != p2)

    sock = socket.socket()
    sock.bind(('localhost', p1))
    eq_(sock.getsockname()[1], p1)
    sock.close()


def test_wait_port():
    port = tcptest.empty_port()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(5)

    tcptest.wait_port(port)
    sock.close()

    # closed socket will not work
    assert_raises(Exception, tcptest.wait_port, port, timeout=0.2)
