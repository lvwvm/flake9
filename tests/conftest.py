"""Test configuration for py.test."""
import sys

import flake9

flake9.configure_logging(2, 'test-logs-%s.%s.log' % sys.version_info[0:2])
