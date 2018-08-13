# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
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
 
from openerp import models, fields , api, tools, _
# from openerp.osv import fields as fields_old
# import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _name = 'product.template'
#   _rec_name='to_yandex'  #  что показывать в крошках и при ссылках
#    _order = 'to_yandex asc'  # порядок показа
    _inherit = ['product.template',]
    _description = 'Шаблон продукта'

    to_yandex = fields.Boolean( 'Передавать в YM', 
                                required=False, 
                                copy=False, 
                                help='Помечаем Продукт, который необходимо выгружать в Yandex.Market'
                                )
#    picture_url = fields.Char('URL изображения', compute='_picture_url', store= True )
    
#    @api.one
##    @api.depends('id','category_id')
#    def _picture_url(self):
#        self.picture_url = 'Test/Test/Test'#self.id + self.category_id
    _rec_name='to_yandex'
    _order = 'to_yandex asc'
    _inherit = [
        'product.template',
        
    ]
    _description = 'Шаблон продукта'
    
    to_yandex = fields.Boolean( 'Передавать в YM', required=False, copy=False, help='Помечаем Продукт, который необходимовыгружать в Yandex.Market')
#    picture_url = ('URL изображения', compute='_picture_url', store= True)
    
#    @api.one
#    @api.depends('stage_id.fold')
#    def _picture_url(self):
#    self.picture_url = self.id + self.category_id
  



