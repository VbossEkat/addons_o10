# -*- coding: utf-8 -*-
##############################################################################
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

class sba_partner(models.Model):
    _inherit = 'res.partner'
    sba_ogrn = fields.Char('ОГРН', size=20, select=True, help= 'ОГРН контрагента')

class sba_company(models.Model):
    _inherit = 'res.company'
    sba_ogrn = fields.Char('ОГРН', size=20, select=True, help= 'ОГРН контрагента')

'''
# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
import werkzeug.utils
import openerp
from openerp.addons.base.ir import ir_qweb

#class Contact(osv.AbstractModel):
class Contact(models.AbstractModel):

    _inherit = 'website.qweb.field.contact'

    def record_to_html_new(self, cr, uid, field_name, record, column, options=None, context=None):
        opf = options.get('fields') or ["name", "address", "phone", "mobile", "fax", "email"]

        if not getattr(record, field_name):
            return None

        id = getattr(record, field_name).id
        field_browse = self.pool[column._obj].browse(cr, openerp.SUPERUSER_ID, id, context={"show_address": True})
        value = werkzeug.utils.escape( field_browse.name_get()[0][1] )

        val = {
            'name': value.split("\n")[0],
            'address': werkzeug.utils.escape("\n".join(value.split("\n")[1:])),
            'phone': field_browse.phone,
            'mobile': field_browse.mobile,
            'fax': field_browse.fax,
            'city': field_browse.city,
            'country_id': field_browse.country_id and field_browse.country_id.name_get()[0][1],
            'email': field_browse.email,
            'fields': opf,
            'options': options
        }

        # my stuff
        if 'inn_kpp' in opf:
            val.update({'inn':field_browse.inn,
                        'kpp':field_browse.kpp})

        if 'bank' in opf:
            val.update({'bank':field_browse.bank_ids[0]})
        # /my stuff

        html = self.pool["ir.ui.view"].render(cr, uid, "base.contact", val, engine='website.qweb', context=context).decode('utf8')

        return ir_qweb.HTMLSafe(html)

    def record_to_html(self, cr, uid, field_name, record, options=None, context=None):
        if context is None:
            context = {}

        if options is None:
            options = {}
        opf = options.get('fields') or ["name", "address", "phone", "mobile", "fax", "email"]

        value_rec = record[field_name]
        if not value_rec:
            return None
        value_rec = value_rec.sudo().with_context(show_address=True)
        value = value_rec.name_get()[0][1]

        val = {
            'name': value.split("\n")[0],
            'address': escape("\n".join(value.split("\n")[1:])),
            'phone': value_rec.phone,
            'mobile': value_rec.mobile,
            'fax': value_rec.fax,
            'city': value_rec.city,
            'country_id': value_rec.country_id.display_name,
            'website': value_rec.website,
            'email': value_rec.email,
            'fields': opf,
            'object': value_rec,
            'options': options
        }

        html = self.pool["ir.ui.view"].render(cr, uid, "base.contact", val, engine='ir.qweb', context=context).decode('utf8')

        return HTMLSafe(html)
'''