
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prometheus-vcgencmd",
    version="0.0.1",
    author="Karl Rink",
    author_email="karl@rink.us",
    description="prometheus-vcgencmd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/krink/prometheus-vcgencmd",
    project_urls={
        "Bug Tracker": "https://gitlab.com/krink/prometheus-vcgencmd/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "console_scripts": ['prometheus-vcgencmd = prometheus_vcgencmd.prometheus_vcgencmd:main']
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)

