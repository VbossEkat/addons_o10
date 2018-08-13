# -*- coding: utf-8 -*-
from openerp import http

# class SeAttrib1(http.Controller):
#     @http.route('/se_attrib1/se_attrib1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/se_attrib1/se_attrib1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('se_attrib1.listing', {
#             'root': '/se_attrib1/se_attrib1',
#             'objects': http.request.env['se_attrib1.se_attrib1'].search([]),
#         })

#     @http.route('/se_attrib1/se_attrib1/objects/<model("se_attrib1.se_attrib1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('se_attrib1.object', {
#             'object': obj
#         })