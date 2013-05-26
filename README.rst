python-tcptest
==============

tcptest is following Perl's "Test::TCP".

It has the methods like original one, but also has another TestServer implementation.

This package also includes memcached and redis test server support.

SYNOPSIS
--------

  import tcptest.memcached
  
  # with context
  with tcptest.memcached.Server() as server:
      memd = memcache.Client(['127.0.0.1:%d' % server.port])
      ...
  
  with tcptest.redis.Server() as server:
      db = redis.Redis(host='127.0.0.1', port=server.port, db=0)
      ...
  
  # manually handling
  server = tcptest.memcached.Server()
  server.start()
  ...
  server.stop()
  
  # custom server
  import tcptest
  
  class YourTestServer(tcptest.TestServer):
      def build_command(self):
          return ('your server command', 'arg1', 'arg2', ...)
  
  with YourTestServer() as server:
      # your server works on server.port
      ...

SEE ALSO
--------

- http://search.cpan.org/~tokuhirom/Test-TCP/
- http://search.cpan.org/~dmaki/Test-Memcached/

Travis
------

.. image :: https://travis-ci.org/nekoya/python-tcptest.png?branch=master
