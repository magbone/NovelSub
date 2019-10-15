#coding: utf-8

from setuptools import setup


setup(
    name="novelsub",
    version="1.0",
    author="magbone",
    author_email="magbone@qq.com",
    description=("A novel subscribe tool"),
    license="MIT",
    packages=['novelsub','novelsub.lib'],

    install_requires=[
        "requests>=2.22.0",
        "APScheduler>=3.6.1"
    ],

    entry_points={
        'console_scripts':[
            'novelsub=novelsub.subscribe:main'
        ]
    }
)