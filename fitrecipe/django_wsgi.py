#!/usr/bin/env python
# coding: utf-8

import os
import sys
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
# 将系统的编码设置为UTF8
reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitrecipe.settings")
import django
django.setup()
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
