# -*- coding: utf-8 -*-

{
    'name': 'sba_payment_moneta',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: Moneta.ru Implementation',
    'version': '1.0',
    'description': """Moneta.ru Payment Acquirer""",
    "author" : "Glukhov VU",
    "website" : "sba-group.ru",
    'depends': ['payment'],
    'data': [
        'views/moneta.xml',
        'views/payment_acquirer.xml',
        'data/moneta.xml',
        'views/payment_moneta_template.xml',
    ],
    'installable': True,
}
