{
    'name': 'Uddogi for Odoo',
    'version': '1.0',
    'summary': 'Here odoo will send structured data for Uddogi throug API',
    'author': 'Nascenia Limited',
    'category': 'Uncategorized',
    'depends': ['base', 'sale', 'purchase', 'account', 'stock'],
    'data': [
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/hs_code_views.xml',
        'views/selling_branch_views.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
            'web.assets_backend': [
                'uddogi-odoo-module/static/src/img/uddogi.png',
            ],
        },
    'installable': True,
    'application': True,
}
