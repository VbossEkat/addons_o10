# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################
 
from openerp import models, fields, api, tools, _
from datetime import datetime, timedelta
# from openerp.osv import fields as fields_old
# import openerp.addons.decimal_precision as dp


class Pofatt(models.Model):
    _name = 'pofatt'
  #  _rec_name='number'
    _description = 'power of attorney'
    number = fields.Char( size=20, string='Number',)
    date_start = fields.Date( string='date_start',default=fields.Date.context_today,)
    date_end = fields.Date( string='date_end',default=datetime.today()+timedelta(days=10),)
    department_id = fields.Many2one('hr.department', ondelete='set null', string='Department', index=True,)
    partner_id = fields.Many2one('res.partner', ondelete='set null', string='Partner',)
    part_hr_employee_id = fields.Many2one('hr.employee', ondelete='set null', string='part_hr_employee',)
    Owner_id = fields.Many2one('hr.employee', ondelete='set null', string='Owner',)
    Emithent_id = fields.Many2one('hr.employee', ondelete='set null', string='Emithent',)
    direction = fields.Selection( string='Direction', selection=[(u'-1', u'Output'), (u'1', u'Input')],default='-1',)
    State = fields.Selection( string='State', selection=[(u'0', u'Draft'), (u'2', u'Used'), (u'3', u'Canceled'), (u'1', u'Confirmed')],default='0',)
    note = fields.Text( string='Note',)
    base = fields.Text( string='Base',)
    pofatt_lines_ids = fields.One2many('pofatt_lines', 'pofatt_id', string='Pofatt_lines',)
    


class PofattLines(models.Model):
    _name = 'pofatt_lines'
    _description = 'pofatt_lines'
    pofatt_id = fields.Many2one('pofatt', ondelete='set null', string='Power of attorney', index=True,)
    product_product_id = fields.Many2one('product.product', ondelete='set null', string='Product',)
    product_uom_id = fields.Many2one('product.uom', ondelete='set null', string='Product unit of measure',)
    price = fields.Float( digits=(15, 4), string='Price',)
    qtt = fields.Float( digits=(15, 4), string='qtt',)
    pofatt_id = fields.Many2one('pofatt', ondelete='set null', string='Power of attorney', index=True,)
    
    


