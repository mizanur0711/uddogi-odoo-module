{
    'name': 'Uddogi for Odoo',
    'version': '1.0',
    'summary': 'Here odoo will send structured data for Uddogi throug API',
    'author': 'Nascenia Limited',
    'category': 'Uncategorized',
    'depends': ['base', 'sale', 'purchase', 'account', 'stock'],
    'data': [
        'views/sale_order_views.xml',
        'views/product_template_views.xml'
    ],
    'installable': True,
    'application': True,
}
