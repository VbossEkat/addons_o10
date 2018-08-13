# -*- coding: utf-8 -*-
from openerp import models, fields , api, tools, _
# from openerp.osv import fields as fields_old
# import openerp.addons.decimal_precision as dp



class Module(models.Model):
    _inherit = "ir.module.module"
    sba_def_module = fields.Boolean( 'Ставить всегда',
                                required=False,
                                copy=False,
                                help='Помечаем Модуль, который ставится в любой конфигурации',
                                default=False
                                )
    @api.multi
    def button_set_default(self):
        for item in self:
            if item.sba_def_module == True:
                item.write({'sba_def_module': False})
            else:
                item.write({'sba_def_module': True})
        return True

#



