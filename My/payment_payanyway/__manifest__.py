# -*- coding: utf-8 -*-
{
    'name': "PayAnyWay Payment Acquirer",
    'category': 'Payment Acquirer',
    'summary': 'Payment Acquirer: PayAnyWay Implementation',

    'description': """
PayAnyWay Payment Acquirer.
    """,

    'author': "PayAnyWay",
    'website': "https://www.payanyway.ru/",

    'version': '1.0',

    'depends': ['payment'],

    'data': [
        'views/payment_views.xml',
        'views/payment_payanyway_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,

    'license': 'LGPL-3',

}

