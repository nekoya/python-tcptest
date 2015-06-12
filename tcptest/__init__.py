# -*- coding: utf-8 -*-
"""
tcptest
~~~~~~~

tcptest is following Perl's "Test::TCP".

It has the methods like original one, but also has another TestServer
implementation.

This package also includes tcptest.memcached module like "Test::Memcached".

- http://search.cpan.org/~tokuhirom/Test-TCP/
- http://search.cpan.org/~dmaki/Test-Memcached/

:author: nekoya <http://nekoya.github.io/>
:license: the MIT License: http://www.opensource.org/licenses/mit-license.php
"""

__version__ = '0.4.0'

import socket
import subprocess
import time


def empty_port():
    """Find an empty port
    Returns:
        <int> empty port
    """
    s = socket.socket()
    s.bind(('', 0))
    (host, port) = s.getsockname()
    s.close()
    return port


def wait_port(port, timeout=3.0):
    """Wait until the port can use
    Args:
        <int> port
        <float> timeout(optional)
    """
    begin = time.time()

    def get_rest_time():
        return max(timeout - (time.time() - begin), 0)

    wait = 0.0001
    while 1:
        try:
            _check_port(port, timeout=get_rest_time())
            break
        except Exception, e:
            if get_rest_time() == 0:
                raise Exception('connect to port:%s timed out. %s' % (port, e))
            wait *= 2
            time.sleep(wait)


def _check_port(port, timeout):
    sock = socket.socket()
    if timeout is not None:
        sock.settimeout(timeout)
    sock.connect(('127.0.0.1', port))
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    sock.close()


class TestServer(object):
    """Test server abstract class"""

    def __init__(self, timeout=3.0, res=None, waiting_returncode_time=0.1):
        """
        Args:
            <float> timeout(optional)
            <dict> stdout/stderr buffer(optional)
        """
        self.timeout = timeout
        self.res = res
        self.waiting_returncode_time = waiting_returncode_time

    def build_command(self):
        """
        Returns:
            <tuple> arguments for popen
        """
        return ()

    def start(self):
        """start test server"""
        self.port = empty_port()
        self._before_start()
        cmd = self.build_command()
        self._proc = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        time.sleep(self.waiting_returncode_time)
        if self._proc.poll():
            err = {
                'stdout': ''.join(self._proc.stdout.readlines()),
                'stderr': ''.join(self._proc.stderr.readlines())
            }
            self.stop()
            raise Exception(err)

        try:
            wait_port(port=self.port, timeout=self.timeout)
        except Exception, e:
            self.stop()
            raise e
        self._after_start()

    def stop(self):
        """stop test server"""
        self._before_stop()
        if not self._proc.poll():
            self._proc.terminate()
        self._wait()
        self._after_stop()

    def _before_start(self):
        """hook event"""
        pass

    def _after_start(self):
        """hook event"""
        pass

    def _before_stop(self):
        """hook event"""
        pass

    def _after_stop(self):
        """hook event"""
        pass

    def _wait(self):
        try:
            (out, err) = self._proc.communicate()
            if self.res is not None:
                self.res['stdout'] = out
                self.res['stderr'] = err
        except KeyboardInterrupt:
            pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, etype, error, exc_info):
        self.stop()
