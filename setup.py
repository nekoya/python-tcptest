from setuptools import setup

setup(
    name='tcptest',
    packages=['tcptest'],
    version='0.1.0',
    author='Ryo Miyake',
    author_email='ryo.studiom@gmail.com',
    description="Testing TCP program, following the Perl's Test::TCP "
                "and Test::Memcached",
    url='http://github.com/nekoya/python-tcptest',
    license='MIT',
    install_requires=['python-memcached'],
    tests_require=['Nose'],
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
