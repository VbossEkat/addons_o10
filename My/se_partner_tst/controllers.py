# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of se_partner_tst, an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     se_partner_tst is free software: you can redistribute it and/or
#     modify it under the terms of the GNU Affero General Public License
#     as published by the Free Software Foundation, either version 3 of
#     the License, or (at your option) any later version.
#
#     se_partner_tst is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the
#     GNU Affero General Public License
#     along with se_partner_tst.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import http

# class SePartnerTst(http.Controller):
#     @http.route('/se_partner_tst/se_partner_tst/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/se_partner_tst/se_partner_tst/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('se_partner_tst.listing', {
#             'root': '/se_partner_tst/se_partner_tst',
#             'objects': http.request.env['se_partner_tst.se_partner_tst'].search([]),
#         })

#     @http.route('/se_partner_tst/se_partner_tst/objects/<model("se_partner_tst.se_partner_tst"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('se_partner_tst.object', {
#             'object': obj
#         })