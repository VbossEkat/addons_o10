# -*- coding: utf-8 -*-
from openerp import models, fields, api
class se_partner_tst(models.Model):
    _inherit = 'product.template'
    x_old_id = fields.Integer('Sequence')
    _inherit = 'product.category'
    ef_grpt = fields.Integer('Product groups')

