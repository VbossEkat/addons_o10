# -*- coding: utf-8 -*-
import pprint
import logging
import urlparse
import urllib2
import werkzeug

from openerp import http, SUPERUSER_ID
from openerp.http import request

_logger = logging.getLogger(__name__)


class MonetaController(http.Controller):
    _return_url = '/shop/payment/'
    _cancel_url = '/shop/'
    _accept_url = '/payment/moneta/feedback/'
    
#     Пример ответа оп проведенной оплате   
#    payURL?
#    http://localhost:8069/payment/moneta/feedback?MNT_ID=94610081&MNT_TRANSACTION_ID=SO071&MNT_OPERATION_ID=390249&MNT_AMOUNT=11.11&MNT_CURRENCY_CODE=RUB&MNT_TEST_MODE=0&MNT_SIGNATURE=69bdf9bd91820b8f7b4c4b25d3d22dfa



    @http.route([
        '/payment/moneta/feedback',
    ], type='http', auth='none')
    def moneta_form_feedback(self, **post):
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
#      _logger.info('Beginning form_feedback with post data %s', pprint.pformat(post))  # debug
        request.registry['payment.transaction'].form_feedback(cr, uid, post, 'moneta', context)
        #return 
        res1 = werkzeug.utils.redirect(post.pop('return_url', '/'))

        res = False
        new_post = dict(post, cmd='_notify-validate')
        cr, uid, context = request.cr, request.uid, request.context
        reference = post.get('MNT_TRANSACTION_ID')
        tx = None
        if reference:
            tx_ids = request.registry['payment.transaction'].search(cr, uid, [('reference', '=', reference)], context=context)
            if tx_ids:
                tx = request.registry['payment.transaction'].browse(cr, uid, tx_ids[0], context=context)
        moneta_urls = request.registry['payment.acquirer']._get_moneta_urls(cr, uid, tx and tx.acquirer_id and tx.acquirer_id.environment or 'prod', context=context)
        validate_url = moneta_urls['moneta_form_url']
        urequest = urllib2.Request(validate_url, werkzeug.url_encode(new_post))
        uopen = urllib2.urlopen(urequest,'SUCCESS')
        resp = uopen.read()
        resp = 'VERIFIED'
        if resp == 'VERIFIED':
            _logger.info('moneta: validated data')
            res = request.registry['payment.transaction'].form_feedback(cr, SUPERUSER_ID, post, 'moneta', context=context)
        elif resp == 'INVALID':
            _logger.warning('moneta: answered INVALID on data verification')
        else:
            _logger.warning('moneta: unrecognized moneta answer, received %s instead of VERIFIED or INVALID' % resp.text)
        return res1


#   def moneta_form_feedback(self, **post):
#        _logger.info('Moneta: entering form_feedback with post data %s', pprint.pformat(post))
#        return_url = '/'
#        if post:
#            request.env['payment.transaction'].sudo().form_feedback(post, 'moneta')
#            return_url = post.pop('return_url', '/')
#        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        # Authorize.Net is expecting a response to the POST sent by their server.
        # This response is in the form of a URL that Authorize.Net will pass on to the
        # client's browser to redirect them to the desired location need javascript.
#        return request.render('sba_payment_moneta.payment_moneta_redirect', {
#            'return_url': '%s' % urlparse.urljoin(base_url, return_url)
#        })

    def moneta_validate_data(self, **post):
        """ moneta IPN: three steps validation to ensure data correctness

         - step 1: return an empty HTTP 200 response -> will be done at the end
           by returning ''
         - step 2: POST the complete, unaltered message back to moneta (preceded
           by cmd=_notify-validate), with same encoding
         - step 3: moneta send either VERIFIED or INVALID (single word)

        Once data is validated, process it. """
        res = False
        new_post = dict(post, cmd='_notify-validate')
        cr, uid, context = request.cr, request.uid, request.context
        reference = post.get('item_number')
        tx = None
        if reference:
            tx_ids = request.registry['payment.transaction'].search(cr, uid, [('reference', '=', reference)], context=context)
            if tx_ids:
                tx = request.registry['payment.transaction'].browse(cr, uid, tx_ids[0], context=context)
        moneta_urls = request.registry['payment.acquirer']._get_moneta_urls(cr, uid, tx and tx.acquirer_id and tx.acquirer_id.environment or 'prod', context=context)
        validate_url = moneta_urls['moneta_form_url']
        urequest = urllib2.Request(validate_url, werkzeug.url_encode(new_post))
        uopen = urllib2.urlopen(urequest)
        resp = uopen.read()
        if resp == 'VERIFIED':
            _logger.info('moneta: validated data')
            res = request.registry['payment.transaction'].form_feedback(cr, SUPERUSER_ID, post, 'moneta', context=context)
        elif resp == 'INVALID':
            _logger.warning('moneta: answered INVALID on data verification')
        else:
            _logger.warning('moneta: unrecognized moneta answer, received %s instead of VERIFIED or INVALID' % resp.text)
        return res

    @http.route('/payment/moneta/ipn/', type='http', auth='none', methods=['POST'])
    def moneta_ipn(self, **post):
        """ moneta IPN. """
        _logger.info('Beginning Moneta IPN form_feedback with post data %s', pprint.pformat(post))  # debug
        self.moneta_validate_data(**post)
        return ''

