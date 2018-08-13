'''
import babel.messages.pofile
import base64
import csv
import datetime
import functools
import glob
import hashlib
import imghdr
import itertools
import jinja2
import json
import logging
import operator
import re
import time
import werkzeug.utils
import werkzeug.wrappers
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO


import odoo.modules.registry
from odoo.api import call_kw, Environment
from odoo.modules import get_resource_path
from odoo.tools import topological_sort
from odoo.tools.translate import _
from odoo.tools.misc import str2bool, xlwt
from odoo.http import content_disposition, dispatch_rpc, request, \
                      serialize_exception as _serialize_exception
from odoo.exceptions import AccessError
from odoo.models import check_method_name

'''

import odoo
from odoo import http
import os
import jinja2
import json
import sys
from odoo.addons.web.controllers.main import Database

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'

db_list = http.db_list

db_monodb = http.db_monodb


if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.web', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps

class Database(Database):
    def _render_template(self, **d):
        d.setdefault('manage',True)
        d['insecure'] = odoo.tools.config['admin_passwd'] == 'admin'
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        # databases list
        d['databases'] = []
        try:
            d['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]
        return env.get_template("sba_database_manager.html").render(d)
