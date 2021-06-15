
# -*- coding: utf-8 -*-

"""name.__main__: executed when this directory is called as script."""

from .prometheus_vcgencmd import Prometheus_Vcgencmd
import sys

def main():
    if sys.argv[1:]:
        if sys.argv[1] == '--version':
            version = Prometheus_Vcgencmd().version()
            print(version)
    else:
        stdout = Prometheus_Vcgencmd().stdout()

if __name__ == "__main__":
    sys.exit(main())

