{
    'name': 'VATSync - Uddogi for Odoo [Bangladesh]',
    'version': '1.0.10',
    'summary': 'Here odoo will send structured data for Uddogi throug API',
    'author': 'Nascenia Limited',
    'category': 'Sales',
    'depends': ['base', 'sale', 'purchase', 'account', 'stock','crm'],
    'website': 'https://nascenia.com/',
    'license': 'LGPL-3',
    'maintainer': 'Nascenia Limited',
    'data': [
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/hs_code_views.xml',
        'views/selling_branch_views.xml',
        'security/ir.model.access.csv',
    ],
    'images':[
        'static/description/banner.png',
            ],
    'assets': {
            'web.assets_backend': [
                'VATSync/static/src/img/uddogi.png',
            ],
        },
    'installable': True,
    'application': True,
}
