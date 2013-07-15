python-tcptest
==============

tcptest is following Perl's "Test::TCP".

It has the methods like original one, but also has another TestServer implementation.

This package also includes memcached and redis test server support.

SYNOPSIS
--------

.. code-block:: python

  import tcptest.memcached
  import tcptest.redis
  
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

TIPS
----

custom server
~~~~~~~~~~~~~

.. code-block:: python

  import tcptest
  
  class YourTestServer(tcptest.TestServer):
      def build_command(self):
          return ('your server command', 'arg1', 'arg2', ...)
  
  with YourTestServer() as server:
      # your server works on server.port
      ...

capture server outputs
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  import tcptest.redis
  
  res = {}
  with tcptest.redis.Server(res=res) as server:
      ...
  stdout = res['stdout']
  stderr = res['stderr']

redis options
~~~~~~~~~~~~~

.. code-block:: python

  import tcptest.redis
  
  with tcptest.redis.Server(settings=dict(databases=4)) as server:
      ...

redis replication
~~~~~~~~~~~~~~~~~

.. code-block:: python

  import tcptest.redis
  
  master = tcptest.redis.Server()
  master.start()

  slave_settings = {'slaveof': 'localhost %d' % master.port}
  slave = tcptest.redis.Server(settings=slave_settings)
  slave.start()

SEE ALSO
--------

- http://search.cpan.org/~tokuhirom/Test-TCP/
- http://search.cpan.org/~dmaki/Test-Memcached/

CHANGES
-------

0.2.4 - 2013/07/16
~~~~~~~~~~~~~~~~~~

- Fix pip installation
    - Add MANIFEST.in

0.2.1-3 - 2013/05/27
~~~~~~~~~~~~~~~~~~~~

- Maintain setup.py and docs

0.2.0 - 2013/05/21
~~~~~~~~~~~~~~~~~~

- Support Redis test server

0.1.0 - 2013/05/21
~~~~~~~~~~~~~~~~~~

- First release

Travis
------

.. image :: https://travis-ci.org/nekoya/python-tcptest.png?branch=master
