
# -*- coding: utf-8 -*-

"""name.__main__: executed when this directory is called as script."""

#from .server import main
#main()


from .prometheus_vcgencmd import Prometheus_Vcgencmd
import sys


def main():
	out = Prometheus_Vcgencmd().version()
	print(out)

if __name__ == "__main__":
	sys.exit(main())


