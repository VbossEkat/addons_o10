# -*- coding: utf-8 -*-
##############################################################################

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
 
# noinspection PyStatementEffect
{
    "name" : "sba_attrib",
    "author" : "VGlukhov SBA",
    "website" : "sba.realstore.ru",
    "category" : "Sales",
    "licence" : "AGPL-3",
    "summary": """
 Модуль для добавлениея аттрибутов, нужных в работе
 1. Добавляет ОГРН, в тч на страницу Контакты
                    """,
    "depends" : ['base_setup'],
    "data" : [
        'views/views.xml',
        ],
    "demo" : [],
    "installable": True,
    "auto_install": False,
    "application": False,
}