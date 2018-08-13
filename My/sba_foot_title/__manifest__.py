{
    'name': "SBA Footer & Copyright",
    'author': 'VGlukhov SBA',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Debranding',
    'website': 'sba.realstore.ru',
    'description': """
    Change the description of the contents of the bottom of the main page
        """,
    'depends': ['web'],
    'data': [
        'views.xml',
        ],
    'qweb': [
        'templ.xml',
        ],
    'auto_install': False,
    'installable': True
}
