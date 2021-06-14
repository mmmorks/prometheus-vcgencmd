
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name = "prometheus-vcgencmd",
    packages = ["prometheus_vcgencmd"],
    entry_points = {
        "console_scripts": ['prometheus-vcgencmd = prometheus_vcgencmd.prometheus_vcgencmd:main']
        },
    version = '0.0.0',
    description = "prometheus-vcgencmd",
    long_description = "prometheus vcgencmd module and exporter",
    author = "Karl Rink",
    author_email = "karl@rink.us",
    url = "https://gitlab.com/krink/prometheus-vcgencmd",
    install_requires = [ ]
    )


