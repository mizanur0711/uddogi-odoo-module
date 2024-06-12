from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    item_hs_code = fields.Many2one('hs.code', string="HS Code", help="Select the HS Code for this product")
    item_inventory_method = fields.Selection([
        ('fifo', 'FIFO'),
        ('lifo', 'LIFO'),
        ('average', 'Average')
    ], string="Inventory Method", default='fifo')

    item_nature = fields.Selection([
        ('zero_rated', 'Zero rated'),
        ('exempted', 'Exempted'),
        ('standard_rated', 'Standard rated'),
        ('based_on_mrp', 'Based on MRP'),
        ('based_on_specific_vat', 'Based on specific VAT'),
        ('other_than_standard_rated', 'Other than Standard rated'),
        ('retail_wholesale_trade_based', 'Retail/Wholesale/Trade based'),
        ('not_admissible_for_credit', 'Not admissible for credit'),
        ('not_admissible_for_credit_exempted', 'Not admissible for credit (who sell only exempted/specific VAT)')
    ], string="Item Nature")
