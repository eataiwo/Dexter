#! /usr/bin/python3.7

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/Github/Dexter/src/web_app')
from remote_control_webapp import app as application
# application.secret_key = 'testing'
