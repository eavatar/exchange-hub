# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="eavatar.hub",
    version="0.1.0",
    description="EAvatar Hub - Rendezvous-based messaging service",
    #package_dir={'': ''},
    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    # install_requires = ['setuptools'],
    test_suite='nose.collector',
    zip_safe=False,

    author="Sam Kuo",
    author_email="sam@eavatar.com",
    url="http://www.eavatar.com",

    entry_points={
        'console_scripts': [
            'hubcli = scripts.hubcli:main',
        ],
    },
)