# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="eavatar.runtime",
    version="0.1.0",
    description="EAvatar Runtime - Basic runtime for EAvatar Hub.",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    # install_requires = ['setuptools'],
    zip_safe=False,

    author="Sam Kuo",
    author_email="sam@eavatar.com",
    url="http://www.eavatar.com",

    entry_points={
        'console_scripts': [
            'hubd = hubd:start',
        ],
    },
)