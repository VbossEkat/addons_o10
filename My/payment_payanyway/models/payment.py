# -*- coding: utf-8 -*-

import hashlib
import urlparse
import locale

from pprint import pformat
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)

class AcquirerPayanyway(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('payanyway', 'PayAnyWay')])
    payanyway_mnt_id = fields.Char(string='Merchant ID', required_if_provider='payanyway', groups='base.group_user')
    payanyway_mnt_secret = fields.Char(string='Code of data integrity verification', required_if_provider='payanyway', groups='base.group_user')
    payanyway_mnt_test_mode = fields.Boolean('Test mode', default=True, help='PayAnyWay test mode', groups='base.group_user')


    def _get_payanyway_urls(self, environment):
        """ PayAnyWay URLs"""
        if environment == 'prod':
            return {'payanyway_form_url': 'https://www.payanyway.ru/assistant.htm'}
        else:
            return {'payanyway_form_url': 'https://demo.moneta.ru/assistant.htm'}

    @api.multi
    def payanyway_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        payanyway_values = dict(values,
                                MNT_ID=str(self.payanyway_mnt_id),
                                MNT_TRANSACTION_ID=str(values['reference']),
                                MNT_AMOUNT=str(locale.format("%.*f", (2, values['amount']))),
                                MNT_DESCRIPTION=values['reference'],
                                MNT_CUSTOM1=values.get('partner_name'),
                                MNT_CUSTOM2=values.get('partner_email'),
                                MNT_CUSTOM3=values.get('partner_phone'),
                                MNT_SUCCESS_URL='%s' % urlparse.urljoin(base_url, '/payment/payanyway/success'),
                                MNT_FAIL_URL='%s' % urlparse.urljoin(base_url, '/payment/payanyway/fail'),
                                MNT_RETURN_URL='%s' % urlparse.urljoin(base_url, '/payment/payanyway/return'),
                                MNT_TEST_MODE=str('1') if self.payanyway_mnt_test_mode else str('0'),
                                MNT_CURRENCY_CODE=str(values['currency'].name)
                                )
        #_logger.info("values:\n"+str(pformat(values)))
        payanyway_values['MNT_SIGNATURE'] = hashlib.md5(
            payanyway_values['MNT_ID'] +
            payanyway_values['MNT_TRANSACTION_ID'] +
            payanyway_values['MNT_AMOUNT'] +
            payanyway_values['MNT_CURRENCY_CODE'] +
            payanyway_values['MNT_TEST_MODE'] +
            str(self.payanyway_mnt_secret)
        ).hexdigest()
        return payanyway_values

    @api.multi
    def payanyway_get_form_action_url(self):
        self.ensure_one()
        return self._get_payanyway_urls(self.environment)['payanyway_form_url']

class TxPayAnyWay(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _payanyway_form_get_tx_from_data(self, data):
        _logger.info("_payanyway_form_get_tx_from_data\n"+pformat(data))
        mnt_transaction_id = data.get('MNT_TRANSACTION_ID')
        order = self.env['payment.transaction'].search([('reference', '=', mnt_transaction_id)])
        if not order or len(order) > 1:
            error_msg = 'PayAnyWay: received data for reference %s' % (mnt_transaction_id)
            if not order:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return order[0]

    # @api.multi
    # def _payanyway_form_get_invalid_parameters(self, data):
    #     invalid_parameters = []
    #     return invalid_parameters

    @api.multi
    def _payanyway_form_validate(self, data):
        self.write({
            'state': 'done',
            'acquirer_reference': data.get('MNT_TRANSACTION_ID'),
        })
        return True
