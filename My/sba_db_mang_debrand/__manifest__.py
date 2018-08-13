{
    'name': "SBA db manager debranding",
    'author': 'SBA Glukhov',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Debranding',
    'website': 'https://sba.realstore.ru',
    'description': """
    Change Title from Odoo to SBAerp &
    debranding database manager
        """,
    'depends': ['base'],
    'data': [
        'js.xml',
        ],
    'auto_install': False,
    'installable': True
}
