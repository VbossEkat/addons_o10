# -*- coding: utf-8 -*-

import base64

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


from openerp.osv import fields, osv
from openerp.tools.translate import _

from openerp import models, fields, api, tools
class se_category(models.Model):
    _inherit = 'product.category'
    ef_grpt = fields.Integer('Группа продукта', select=True)
    ef_kat_vidt = fields.Integer('Категория продукта', select=True)
    ef_kat_vidt_kat_grpt_kod = fields.Integer('Родительская категория продукта', select=True)
class se_template(models.Model):
    _inherit = 'product.template'
    ef_id = fields.Integer('Код продукта из ЛО', select=True)
    ef_def_code = fields.Char('Артикул из ЛО', size=10, select=True)
class se_product(models.Model):
    _inherit = 'product.product'
    ef_id = fields.Integer('Код продукта из ЛО', select=True)
#    ef_def_code = fields.Char('Артикул из ЛО', size=10, select=True)
class se_partner(models.Model):
    _inherit = 'res.partner'
    ef_id = fields.Integer('Код контрагента из ЛО', select=True)
    ef_id_adr = fields.Integer('Код адреса из KLN_ADK', select=True)
    ef_id_sot = fields.Integer('Код сотрудника из ЛО', select=True)
class product_pricelist(models.Model):
    _inherit = 'product.pricelist'
    ef_is_comp = fields.Boolean('ЭтоАкция', select=True)
    ef_partnerid = fields.Many2one('res.partner', ondelete='set null', string='Контрагент', select=True)
class product_pricelist_version(models.Model):
    _inherit = 'product.pricelist.version'
    state = fields.Selection([
            ('draft', 'Черновик'),
            ('confirmed', 'Утвержден'),
            ('progress', 'Действующая'),
            ('finished', 'ЗАВЕРШЕНА'),
            ],default='draft', size=10, select=True)
    #This function is triggered when the user clicks on the button 'Черновик'
    #@api.one
    def draft_progressbar(self):
        self.write({
            'state': 'draft',
        })
     
    #This function is triggered when the user clicks on the button 'Утвержден'
    #@api.one
    def confirmed_progressbar11(self):
        self.write({
        'state': 'confirmed'
        })
     
    #This function is triggered when the user clicks on the button 'Действующая'
    @api.one
    def progress_progressbar(self):
        self.satate = 'progress'
        return True
     #   self.write({
     #   'state': 'progress'
     #   })
     
    #This function is triggered when the user clicks on the button 'ЗАВЕРШЕНА'
    @api.one
    def finished_progressbar(self):
        self.satate = 'finished'
        return True
    
    '''
        self.write({
        'state': 'finished',
        })
    '''
class hr_department(models.Model):
    _inherit = 'hr.department'
    ef_id = fields.Integer('Код отдела из ЛО', select=True)
class hr_employee(models.Model):
    _inherit = 'hr.employee'
    ef_id = fields.Integer('Код сотрудника из ЛО', select=True)
class res_users(models.Model):
    _inherit = 'res.users'
    ef_id_sot = fields.Integer('Код сотрудника из ЛО', select=True)
class resource_resource(models.Model):
    _inherit = 'resource.resource'
    ef_id_sot = fields.Integer('Код сотрудника из ЛО', select=True)
class res_company(models.Model):
    _inherit = 'res.company'
    ef_id = fields.Integer('Код клиента из KAT_KLN ЛО', select=1)
class account_bank_statement(models.Model):
    _inherit = 'account.bank.statement'
    rch_b = fields.Char('Расчетный счет из ЛО',size=20, select=True)
class account_invoice(models.Model):
    _inherit = 'account.invoice'
 #   ef_id = fields.Integer('Код строки из LIST_SKL ЛО')
  #  ставим вручную bigint
class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
  #  ef_id = fields.Integer('Код строки из HIST_SKL ЛО')
  #  ef_list_id = fields.Integer('Код строки из LIST_SKL ЛО')
  #  ставим вручную bigint
class stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'
    ef_id = fields.Integer('Код строки из KAT_SKL ЛО', select=True)

class pricelist_se_import(models.Model):
    _name = 'product.pricelist.import'
    _description = 'Import PriceList file'
    file_data  = fields.Binary('Import PriceList File' , required=True)
    file_fname = fields.Char('Import PriceList Filename', size=128, required=True)
    note = fields.Text('Log')

    _defaults = {
        'file_fname': lambda *a: '',
    }
""""
    def file_parsing(self, cr, uid, ids, context=None, batch=False, rfile=None, rfilename=None):
        if context is None:
            context = {}
        if batch:
            rfile = str(rfile)
            rfilename = rfilename
        else:
            data = self.browse(cr, uid, ids)[0]
            try:
                rfile = data.file_data
                rfilename = data.file_fname
            except:
                raise osv.except_osv(_('Error'), _('Wizard in incorrect state. Please hit the Cancel button'))
                return {}
        recordlist = unicode(base64.decodestring(rfile), 'windows-1251', 'strict').split('\n')
        strobj = []
        for line in recordlist:
            strobj.append(line.split('='))

        format_import_file = ''
        encoding_file = ''
        statements = {}
        note = []
        inc_desc = 1
        if rmspaces(recordlist[0]) != '1CClientBankExchange':
            raise osv.except_osv(_('Error'), _('Incorrect description of import file'))

        if strobj[inc_desc][0] == u'ВерсияФормата':
            format_import_file = rmspaces(strobj[inc_desc][1])
            note.append(recordlist[inc_desc] + '\n')
            inc_desc+=1
        else:
            raise osv.except_osv(_('Error'), _('Incorrect description of import file'))

        if strobj[inc_desc][0] == u'Кодировка':
            encoding_file = rmspaces(strobj[inc_desc][1])
            note.append(recordlist[inc_desc] + '\n')
            inc_desc+=1
        else:
            raise osv.except_osv(_('Error'), _('Incorrect description of import file'))

        if strobj[inc_desc][0] == u'Отправитель':
            note.append(recordlist[inc_desc] + '\n')
            inc_desc+=1
        if strobj[inc_desc][0] == u'Получатель':
            note.append(recordlist[inc_desc] + '\n')
            inc_desc+=1
        else:
            raise osv.except_osv(_('Error'), _('Incorrect description of import file'))
        
        if strobj[inc_desc][0] == u'ДатаСоздания':
            note.append(recordlist[inc_desc] + '\n')
            inc_desc+=1
        if strobj[inc_desc][0] == u'ВремяСоздания':
            note.append(recordlist[inc_desc] + '\n')
            inc_desc+=1

        if strobj[inc_desc][0] == u'ДатаНачала':
            note.append(recordlist[inc_desc] + '\n')
            statements['begin_date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT, time.strptime(rmspaces(strobj[inc_desc][1]),'%d.%m.%Y'))
            inc_desc+=1
        else:
            raise osv.except_osv(_('Error'), _('Incorrect description of import file'))
        if strobj[inc_desc][0] == u'ДатаКонца':
            note.append(recordlist[inc_desc] + '\n')
            statements['end_date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT, time.strptime(rmspaces(strobj[inc_desc][1]),'%d.%m.%Y'))
            inc_desc+=1
        else:
            raise osv.except_osv(_('Error'), _('Incorrect description of import file'))
        acc_numbers = []
        while strobj[inc_desc][0] == u'РасчСчет':
            acc_number = {}
            acc_number['detail'] = []
            acc_number['statement_line'] = []
            acc_number['acc_number'] = rmspaces(strobj[inc_desc][1])
            acc_number['journal_id'] = False
            acc_number['bank_account'] = False
            bank_ids = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number', '=', acc_number['acc_number'])])
            if bank_ids and len(bank_ids) > 0:
                bank_accs = self.pool.get('res.partner.bank').browse(cr, uid, bank_ids)
                for bank_acc in bank_accs:
                    if bank_acc.journal_id.id:
                        acc_number['journal_id'] = bank_acc.journal_id
                        acc_number['bank_account'] = bank_acc
                        break
            if not acc_number['bank_account']:
                raise osv.except_osv(_('Error'), _("No matching Bank Account (with Account Journal) found.\n\nPlease set-up a Bank Account with as Account Number '%s' and an Account Journal.") % (acc_number['acc_number']))
            acc_numbers.append(acc_number)
            inc_desc+=1
        def acc_number_parsing(obj, line_number):
            acc_res = {}
            acc_res_number = ''
            while rmspaces(obj[line_number][0]) != u'КонецРасчСчет':
                if obj[line_number][0] == u'ДатаНачала':
                    acc_res['begin_date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT, time.strptime(rmspaces(obj[line_number][1]),'%d.%m.%Y'))
                elif obj[line_number][0] == u'ДатаКонца':
                    acc_res['end_date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT, time.strptime(rmspaces(obj[line_number][1]),'%d.%m.%Y')) 
                elif obj[line_number][0] == u'РасчСчет':
                    acc_res_number = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'НачальныйОстаток':
                    acc_res['balance_start'] = float(rmspaces(obj[line_number][1]))
                elif obj[line_number][0] == u'ВсегоПоступило':
                    acc_res['balance_plus'] = float(rmspaces(obj[line_number][1]))
                elif obj[line_number][0] == u'ВсегоСписано':
                    acc_res['balance_minus'] = float(rmspaces(obj[line_number][1]))
                elif obj[line_number][0] == u'КонечныйОстаток':
                    acc_res['balance_end'] = float(rmspaces(obj[line_number][1]))
                line_number += 1
            line_number += 1
            return acc_res_number, acc_res, line_number
        def statement_line_parsing(obj, line_number):
            statementLine = {}
            statementLine['note'] = []
            while rmspaces(obj[line_number][0]) != u'КонецДокумента':
                if obj[line_number][0] == u'Номер':
                    statementLine['ref'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'Дата':
                    statementLine['date'] = time.strftime(tools.DEFAULT_SERVER_DATE_FORMAT, time.strptime(rmspaces(obj[line_number][1]),'%d.%m.%Y'))
                elif obj[line_number][0] == u'Сумма':
                    statementLine['amount'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'ПлательщикСчет':
                    statementLine['payer_acc'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'Плательщик1' or obj[line_number][0] == u'Плательщик':
                    statementLine['payer'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'ПлательщикИНН':
                    statementLine['payer_inn'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'ПолучательСчет':
                    statementLine['recipient_acc'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'Получатель1' or obj[line_number][0] == u'Получатель':
                    statementLine['recipient'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'ПолучательИНН':
                    statementLine['recipient_inn'] = rmspaces(obj[line_number][1])
                elif obj[line_number][0] == u'НазначениеПлатежа':
                    statementLine['name'] = rmspaces(obj[line_number][1])
                else:
                    statementLine['note'].append(obj[line_number][0] + ': ' + obj[line_number][1])
                line_number += 1
            line_number += 1
            return statementLine, line_number

        i = inc_desc
        while rmspaces(strobj[i][0]) != u'КонецФайла':
            if rmspaces(strobj[i][0]) == u'СекцияРасчСчет':
                tmp_acc, tmp_acc_res, i = acc_number_parsing(strobj, i)
                for acc_one in acc_numbers:
                    if acc_one['acc_number'] == tmp_acc:
                        acc_one['detail'].append(tmp_acc_res)
                        break
            elif strobj[i][0] == u'СекцияДокумент':
                tmp_statementLine, i = statement_line_parsing(strobj, i)
                for acc_one in acc_numbers:
                    if acc_one['acc_number'] == tmp_statementLine['payer_acc'] or acc_one['acc_number'] == tmp_statementLine['recipient_acc']:
                        tmp_statementLine['sequence'] = len(acc_one['statement_line']) + 1
                        acc_one['statement_line'].append(tmp_statementLine)
                        break
            i += 1

        for i, statement in enumerate(acc_numbers):
            for acc_detail in statement['detail']:
                if acc_detail['begin_date'] == statements['begin_date']:
                    statement['balance_start'] = acc_detail['balance_start']
                if acc_detail['end_date'] == statements['end_date']:
                    statement['balance_end'] = acc_detail['balance_end']

            period_id = self.pool.get('account.period').search(cr, uid, [('company_id', '=', statement['journal_id'].company_id.id), ('date_start', '<=', statements['end_date']), ('date_stop', '>=', statements['end_date'])])
            if not period_id and len(period_id) == 0:
                raise osv.except_osv(_('Error'), _("The Statement New Balance date doesn't fall within a defined Accounting Period! Please create the Accounting Period for date %s for the company %s.") % (statements['end_date'], statement['journal_id'].company_id.name))
            statement['period_id'] = period_id[0]

            statement['note'] = note
            cr.execute('SELECT balance_end_real \
            FROM account_bank_statement \
            WHERE journal_id = %s and date <= %s \
            ORDER BY date DESC,id DESC LIMIT 1', (statement['journal_id'].id, statements['begin_date']))
            res = cr.fetchone()
            balance_start_check = res and res[0]
            if balance_start_check == None:
                if statement['journal_id'].default_debit_account_id and (statement['journal_id'].default_credit_account_id == statement['journal_id'].default_debit_account_id):
                    balance_start_check = statement['journal_id'].default_debit_account_id.balance
                else:
                    raise osv.except_osv(_('Error'), _("Configuration Error in journal %s!\nPlease verify the Default Debit and Credit Account settings.") % statement['journal_id'].name)
            if statement.get('balance_start'):
                if balance_start_check != statement['balance_start']:
                    statement['note'].append(_("The Statement %s Starting Balance (%.2f) does not correspond with the previous Closing Balance (%.2f) in journal %s!") % (statement['acc_number'] + ' #' + statements['begin_date'] + ':' + statements['end_date'], statement['balance_start'], balance_start_check, statement['journal_id'].name))
                else:
                    statement['note'].append(_("Not found Balance Start value."))
            if not(statement.get('period_id')):
                raise osv.except_osv(_('Error'), _(' No transactions or no period in file !'))
            data = {
                'name': statement['acc_number'] + ' #' + statements['begin_date'] + ':' + statements['end_date'],
                'date': datetime.now(),
                'journal_id': statement['journal_id'].id,
                'period_id': statement['period_id'],
                'balance_start': statement['balance_start'] if statement.get('balance_start') else False,
                'balance_end_real': statement['balance_end'],
            }
            statement['id'] = self.pool.get('account.bank.statement').create(cr, uid, data, context=context)
            for line in statement['statement_line']:
                partner = None
                partner_id = None
                bank_account_id = None
                invoice = False
                if line['payer_acc'] == statement['acc_number']:
                    ids = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number', '=', str(line['recipient_acc']))])
                    if ids and len(ids) > 0:
                        bank_account_id = ids[0]
                        partner = self.pool.get('res.partner.bank').browse(cr, uid, ids[0], context=context).partner_id
                        partner_id = partner.id
                        line['account'] = partner.property_account_payable.id
                        if partner.supplier:
                            line['transaction_type'] = 'supplier'
                        else:
                            line['transaction_type'] = 'general'
                    #ids = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number', '=', str(line['counterpartyNumber']))])
                    if not partner and not invoice:
                        line['name'] = line['name'] + '\n' + line['recipient']
                    if 'voucher_id' not in line:
                        line['voucher_id'] = None
                    if 'transaction_type' not in line:
                        line['transaction_type'] = 'general'
                    data = {
                        'name': line['name'],
                        'note': '\n'.join(line['note']),
                        'date': line['date'],
                        'amount': '-' + line['amount'],
                        'partner_id': partner_id,
                        #'account_id': line['account'],
                        'statement_id': statement['id'],
                        'ref': line['ref'],
                        'sequence': line['sequence'],
                        'bank_account_id': bank_account_id,
                    }
                    data_check = {
                        'date': line['date'],
                        'amount': '-' + line['amount'],
                        'ref': line['ref'],
                        #'account_id': line['account'],
                    }
                else:
                    ids = self.pool.get('res.partner.bank').search(cr, uid, [('acc_number', '=', str(line['payer_acc']))])
                    if ids and len(ids) > 0:
                        partner = self.pool.get('res.partner.bank').browse(cr, uid, ids[0], context=context).partner_id
                        partner_id = partner.id
                        line['account'] = partner.property_account_receivable.id
                        if partner.customer:
                            line['transaction_type'] = 'customer'
                        else:
                            line['transaction_type'] = 'general'
                    else:
                        #create the bank account, not linked to any partner. The reconciliation will link the partner manually
                        #chosen at the bank statement final confirmation time.
                        try:
                            type_model, type_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base', 'bank_normal')
                            type_id = self.pool.get('res.partner.bank.type').browse(cr, uid, type_id, context=context)
                            bank_code = type_id.code
                        except ValueError:
                            bank_code = 'bank'
                        bank_account_id = self.pool.get('res.partner.bank').create(cr, uid, {'acc_number': str(line['payer_acc']), 'state': bank_code}, context=context)
                    if not partner and not invoice:
                        line['name'] = line['name'] + '\n' + line['payer']
                    if 'voucher_id' not in line:
                        line['voucher_id'] = None
                    if 'transaction_type' not in line:
                        line['transaction_type'] = 'general'
                    data = {
                        'name': line['name'],
                        'note': '\n'.join(line['note']),
                        'date': line['date'],
                        'amount': line['amount'],
                        'partner_id': partner_id,
                        #'account_id': line['account'],
                        'statement_id': statement['id'],
                        'ref': line['ref'],
                        'sequence': line['sequence'],
                        'bank_account_id': bank_account_id,
                    }
                    data_check = {
                        'date': line['date'],
                        'amount': line['amount'],
                        'ref': line['ref'],
                        #'account_id': line['account'],
                    }
                ids_line_statement = self.pool.get('account.bank.statement.line').search(cr, uid, [('date','=',data_check['date']),('amount','=',data_check['amount']),('ref','=',data_check['ref'])])
                if ids_line_statement:
                    statement['note'].append(_('Statement line %s from %s alredy exist.')%(data_check['ref'], data_check['date']))
                else:
                    self.pool.get('account.bank.statement.line').create(cr, uid, data, context=context)
                    
            if statement['note']:
                self.pool.get('account.bank.statement').write(cr, uid, [statement['id']], {'rusimport_note': '\n'.join(statement['note'])}, context=context)
        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account', 'action_bank_reconcile_bank_statements')
        action = self.pool[model].browse(cr, uid, action_id, context=context)
        statements_ids = [statement['id'] for statement in acc_numbers]
        return {
            'name': action.name,
            'tag': action.tag,
            'context': {'statement_ids': statements_ids},
            'type': 'ir.actions.client',
        }

def rmspaces(s):
    return " ".join(s.split())
"""    


'''
                               <!--The header tag is built to add buttons within. This puts them at the top -->
                            <header>
                                <button string="В черновик" type="object" name="draft_progressbar" attrs="{'invisible': [('state', '=', 'draft')]}"/>
                                <!--The oe_highlight class gives the button a red color when it is saved.
                                It is usually used to indicate the expected behaviour. -->
                                <button string="Утверждено" type="object" name="confirmed_progressbar" class="oe_highlight" attrs="{'invisible': [('state','!=','draft')]}"/>
                                <button string="Действующая" type="object" name="progress_progressbar" attrs="{'invisible': [('state','=','progress')]}"/>
                                <button string="Завершена" type="object" name="finished_progressbar" attrs="{'invisible': [('state','=','finished')]}"/>
                                <!--This will create the statusbar, thanks to the widget. -->
                                <field name="state" widget="statusbar"/>
                            </header>
   Заготовка для бара                         
                            
'''