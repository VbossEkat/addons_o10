# -*- coding: utf-8 -*-
from odoo import http

class TestPage(http.Controller):
    @http.route('/test-page/',auth='public', website=True)
    def index(self,**kw):
        return http.request.render('sba_testpage.test_index')
