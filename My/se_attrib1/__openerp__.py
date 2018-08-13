# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of se_partner_tst,
#     an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     se_partner_tst is free software:
#     you can redistribute it and/or modify it under the terms of the GNU
#     Affero General Public License as published by the Free Software
#     Foundation,either version 3 of the License, or (at your option) any
#     later version.
#
#     se_partner_tst is distributed
#     in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
#     even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with se_partner_tst.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "se_attribute",

    'summary': """
        Добавляем поля для синхронизации с ЛО """,

    # 'description': put the module description in README.rst

    'author': 'Глухов В.Ю.,'
              'SE',
    'website': "http://sed24.ru",

    # Categories can be used to filter modules in modules listing
    # Check http://goo.gl/0TfwzD for the full list
    'category': 'Uncategorized',
    'version': '0.0.0.0.4',
    # any module necessary for this one to work correctly
    'depends': ['base','product','account_voucher','account',],
    #,'stock'
    'data': ['se_views_menu.xml',],
    'license': 'AGPL-3', 
}
