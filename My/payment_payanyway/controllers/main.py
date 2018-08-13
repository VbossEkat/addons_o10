# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug
import hashlib

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PayAnyWayController(http.Controller):
    @http.route(['/payment/payanyway/return'], type='http', auth='public', csrf=False)
    def payanyway_return(self, **post):
        """ PayAnyWay."""
        _logger.debug(
            'PayAnyWay: entering payanyway_return with post data %s', pprint.pformat(post))
        return_url = '/'
        return werkzeug.utils.redirect(return_url)

    @http.route(['/payment/payanyway/payurl'], type='http', auth='public', csrf=False)
    def payanyway_payurl(self, **post):
        _logger.debug(
            'PayAnyWay: entering payanyway_payurl with post data %s', pprint.pformat(post))
        mnt_transaction_id = post.get('MNT_TRANSACTION_ID')
        order = request.env['payment.transaction'].search([('reference', '=', mnt_transaction_id)])
        if not order or len(order) > 1:
            return 'FAIL'
        order = order[0]
        mnt_id = str(post.get('MNT_ID'))
        mnt_operation_id = str(post.get('MNT_OPERATION_ID'))
        mnt_amount = str(post.get('MNT_AMOUNT'))
        mnt_currency_code = str(post.get('MNT_CURRENCY_CODE'))
        mnt_subscriber_id = str(post.get('MNT_SUBSCRIBER_ID'))
        mnt_test_mode = str(post.get('MNT_TEST_MODE'))
        mnt_signature = str(post.get('MNT_SIGNATURE'))
        pa = request.env['payment.acquirer'].sudo().search([('provider', '=', 'payanyway')], limit=1);
        mnt_secret = str(pa.payanyway_mnt_secret)
        mnt_signature_calculated = hashlib.md5(
            mnt_id + mnt_transaction_id + mnt_operation_id + mnt_amount + mnt_currency_code + mnt_subscriber_id + mnt_test_mode + mnt_secret
        ).hexdigest()
        if (mnt_signature == mnt_signature_calculated):
            request.env['payment.transaction'].sudo().form_feedback(post, 'payanyway')
            return 'SUCCESS'
        else:
            return 'FAIL'
