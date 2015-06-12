from setuptools import setup

setup(
    name='tcptest',
    packages=['tcptest'],
    version='0.5.0',
    author='Ryo Miyake',
    author_email='ryo.studiom@gmail.com',
    description="Testing TCP program, following the Perl's Test::TCP "
                "include memcached and redis test server.",
    long_description=open('README.rst').read(),
    url='http://github.com/nekoya/python-tcptest',
    license='MIT',
    tests_require=['Nose', 'python-memcached', 'redis', 'fluent-logger'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
    ],
)
