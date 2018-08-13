{
    'name': "SBA POS costumization",
    'author': 'SBA Glukhov',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Debranding',
    'website': 'https://sba.realstore.ru',
    'description': """
    Change Title to SBAerp 
    Change logo.png
        """,
    'depends': ['point_of_sale'],
    'data': [
        'views.xml',
        ],
    'qweb': [
        'static/src/xml/pos_logo.xml',
    ],
    'auto_install': False,
    'installable': True
}
