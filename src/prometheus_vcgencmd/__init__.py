
# -*- coding: utf-8 -*-


from .prometheus_vcgencmd import *

import subprocess
try:
	subprocess.check_output("vcgencmd")
except Exception:
	raise ImportError("\"vcgencmd\" command not found")


