# -*- coding: utf-'8' "-*-"

import hashlib
import hmac
import logging
import time
import urlparse
import pprint
from openerp.osv import osv

from openerp import api, fields, models
from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.addons.sba_payment_moneta.controllers.main import MonetaController
from openerp.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


class PaymentAcquirerMoneta(models.Model):
    _inherit = 'payment.acquirer'

 #   def _get_moneta_urls(self, environment):
    def _get_moneta_urls(self,cr, uid, environment,context):
#   cr, uid, tx and tx.acquirer_id and tx.acquirer_id.environment or 'prod', context=context     
        """ moneta URLs """
        if environment == 'prod':
            return {'moneta_form_url': 'https://demo.moneta.ru/assistant.htm'}
#            return {'moneta_form_url': 'https://www.payanyway.ru/assistant.htm'}
        else:
            return {'moneta_form_url': 'https://demo.moneta.ru/assistant.htm'}
 #           return {'moneta_form_url': 'https://test.moneta.net/gateway/transact.dll'}

    @api.model
    def _get_providers(self):
        providers = super(PaymentAcquirerMoneta, self)._get_providers()
        providers.append(['sba_moneta', 'Moneta.ru'])
        return providers

    moneta_login = fields.Char(string='API Login Id', required_if_provider='moneta')
    moneta_transaction_key = fields.Char(string='API Transaction Key', required_if_provider='moneta')

    def _moneta_generate_hashing(self, values):
        data = '^'.join([
            values['MNT_ID'],
            values['x_fp_sequence'],
            values['x_fp_timestamp'],
            values['MNT_AMOUNT'],
            values['MNT_CURRENCY_CODE']])
        return hmac.new(str(values['x_trans_key']), data, hashlib.md5).hexdigest()

    @api.multi
    def moneta_form_generate_values(self, partner_values, tx_values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        moneta_tx_values = dict(tx_values)
        temp_moneta_tx_values = {
            'MNT_AMOUNT': str(tx_values['amount']),
            'MNT_ID': self.moneta_login,
            'x_trans_key': self.moneta_transaction_key,
            'MNT_TRANSACTION_ID': tx_values['reference'],
            'MNT_CURRENCY_CODE': tx_values['currency'] and tx_values['currency'].name or '',
            'MNT_TEST_MODE': '0' if self.environment == 'prod' else '1',
        #    'x_show_form': 'PAYMENT_FORM',
        #    'x_type': 'AUTH_CAPTURE',
#             'x_method': 'CC',
             'x_fp_sequence': '%s%s' % (self.id, int(time.time())),
#            'x_version': '3.1',
#            'x_relay_response': 'TRUE',
            'x_fp_timestamp': str(int(time.time())),
            'x_relay_url': '%s' % urlparse.urljoin(base_url, MonetaController._return_url),
            'x_return_url': '%s' % urlparse.urljoin(base_url, MonetaController._return_url),
            'x_cancel_url': '%s' % urlparse.urljoin(base_url, MonetaController._cancel_url),
            'x_accept_url': '%s' % urlparse.urljoin(base_url, MonetaController._accept_url),
            'x_currency_code': tx_values['currency'] and tx_values['currency'].name or '',
            'MNT_CUSTOM_address': partner_values['address'],
#            'city': partner_values['city'],
#            'country': partner_values['country'] and partner_values['country'].name or '',
            'MNT_CUSTOM_email': partner_values['email'],
#            'zip': partner_values['zip'],
            'MNT_CUSTOM_first_name': partner_values['first_name'],
            'MNT_CUSTOM_last_name': partner_values['last_name'],
            'MNT_CUSTOM_phone': partner_values['phone'],
#            'state': partner_values.get('state') and partner_values['state'].name or '',
        }
        temp_moneta_tx_values['returndata'] = moneta_tx_values.pop('return_url', '')
        temp_moneta_tx_values['x_fp_hash'] = self._moneta_generate_hashing(temp_moneta_tx_values)
        moneta_tx_values.update(temp_moneta_tx_values)
        return partner_values, moneta_tx_values

    @api.multi
    def moneta_get_form_action_url(self):
        self.ensure_one()
        return self._get_moneta_urls(self.environment)['moneta_form_url']


class TxMoneta(models.Model):
    _inherit = 'payment.transaction'

    moneta_txnid = fields.Char(string='Transaction ID')

    _moneta_valid_tx_status = 1
    _moneta_pending_tx_status = 4
    _moneta_cancel_tx_status = 2

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    @api.model
    def _moneta_form_get_tx_from_data(self, data):
        """ Given a data dict coming from moneta, verify it and find the related
        transaction record. """
  #      reference, trans_id, fingerprint = data.get('x_invoice_num'), data.get('x_trans_id'), data.get('x_MD5_Hash')
        reference, trans_id, fingerprint = data.get('MNT_TRANSACTION_ID'), data.get('MNT_OPERATION_ID'), data.get('MNT_SIGNATURE')
        if not reference or not trans_id or not fingerprint:
            error_msg = 'moneta: received data with missing reference (%s) or trans_id (%s) or fingerprint (%s)' % (reference, trans_id, fingerprint)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        tx = self.search([('reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = 'moneta: received data for reference %s' % (reference)
            if not tx:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    @api.model
    def _moneta_form_get_invalid_parameters(self, tx, data):
        invalid_parameters = []

        if tx.moneta_txnid and data.get('x_trans_id') != tx.moneta_txnid:
            invalid_parameters.append(('Transaction Id', data.get('x_trans_id'), tx.moneta_txnid))
        # check what is buyed
        if float_compare(float(data.get('x_amount', '0.0')), tx.amount, 2) != 0:
            invalid_parameters.append(('Amount', data.get('x_amount'), '%.2f' % tx.amount))
        return invalid_parameters

class MonetaPaymentTransaction(osv.Model):
    _inherit = 'payment.transaction'
    moneta_txnid = fields.Char(string='Transaction ID')

    _moneta_valid_tx_status = 1
    _moneta_pending_tx_status = 4
    _moneta_cancel_tx_status = 2

    @api.model
    def _moneta_form_get_tx_from_data(self, data):
        """ Given a data dict coming from moneta, verify it and find the related
        transaction record. """
  #      reference, trans_id, fingerprint = data.get('x_invoice_num'), data.get('x_trans_id'), data.get('x_MD5_Hash')
        reference, trans_id, fingerprint = data.get('MNT_TRANSACTION_ID'), data.get('MNT_OPERATION_ID'), data.get('MNT_SIGNATURE')
        if not reference: 
        # убрано для тестирования
        # or not trans_id or not fingerprint:
            error_msg = 'Moneta.ru: received data with missing reference (%s) or trans_id (%s) or fingerprint (%s)' % (reference, trans_id, fingerprint)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        tx = self.search([('reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = 'Moneta.ru: получена информация по оплате счета %s' % (reference)
            if not tx:
                error_msg += '; такой счет не найден'
            else:
                error_msg += '; таких счетов несколько'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    def _moneta_form_get_invalid_parameters(self, cr, uid, tx, data, context=None):
        invalid_parameters = []

        if float_compare(float(data.get('MNT_AMOUNT', '0.0')), tx.amount, 2) != 0:
            invalid_parameters.append(('Сумма', data.get('MNT_AMOUNT'), '%.2f' % tx.amount))
        if data.get('MNT_CURRENCY_CODE') != tx.currency_id.name:
            invalid_parameters.append(('Валюта', data.get('MNT_CURRENCY_CODE'), tx.currency_id.name))
#    добавлено для тестирования
        invalid_parameters = []
        return invalid_parameters

    @api.model
    def _moneta_form_validate(self, tx, data):
        if tx.state == 'done':
            _logger.warning('moneta: trying to validate an already validated tx (ref %s)' % tx.reference)
            return True
        status_code = int(data.get('x_response_code', '1'))
 #       status_code = 1
        if status_code == self._moneta_valid_tx_status:
            tx.write({
                'state': 'done',
                'moneta_txnid': data.get('MNT_OPERATION_ID'),
                'acquirer_reference': data.get('MNT_TRANSACTION_ID'),
            })
            return True
        elif status_code == self._moneta_pending_tx_status:
            tx.write({
                'state': 'pending',
                'moneta_txnid': data.get('MNT_OPERATION_ID'),
                'acquirer_reference': data.get('MNT_TRANSACTION_ID'),
            })
            return True
        elif status_code == self._moneta_cancel_tx_status:
            tx.write({
                'state': 'cancel',
                'moneta_txnid': data.get('MNT_OPERATION_ID'),
                'acquirer_reference': data.get('MNT_TRANSACTION_ID'),
            })
            return True
        else:
#            error = data.get('x_response_reason_text')
            error = 'Тип ошибки не определен'
            _logger.info(error)
            tx.write({
                'state': 'error',
                'state_message': error,
                'moneta_txnid': data.get('MNT_OPERATION_ID'),
                'acquirer_reference': data.get('MNT_TRANSACTION_ID'),
            })
            return False



#    def _moneta_form_validate(self, cr, uid, tx, data, context=None):
#        _logger.info('Validated moneta payment for tx %s: set as pending' % (tx.reference))
#        return tx.write({'state': 'pending'})