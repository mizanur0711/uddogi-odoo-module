
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
        'views/date_range_wizard_views.xml',
        'views/message_notification_views.xml',
        'views/vat_bangladesh_action_menu.xml',
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/hs_code_views.xml',
        'views/selling_branch_views.xml',
        # 'views/vat_tour_views.xml',
        'views/res_config_settings_views.xml',
        'security/ir.model.access.csv',
    ],
    'images':[
        'static/description/banner.png',
            ],
    'assets': {
            'web.assets_backend': [
                'VATSync/static/src/img/uddogi.png',
                'VATSync/static/src/css/custom_style.css',
                'VATSync/static/src/js/generate_mushak.js',
                # 'VATSync/static/src/js/start_vat_tour.js',
            ],
        },
    'installable': True,
    'application': True,
}
