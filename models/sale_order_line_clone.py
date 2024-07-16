from odoo import models, fields, api

class SaleOrderLineClone(models.Model):
    _name = 'sale.order.line.clone'
    _description = 'Sale Order Line Clone'

    order_id = fields.Many2one('sale.order', string="Order Reference", required=True, ondelete='cascade', index=True, copy=False)
    product_template_id = fields.Many2one('product.template', string="Product Template", required=True)
    name = fields.Char(string="Description", required=True)
    sd_percentage = fields.Float(string="SD (%)", related='product_template_id.hs_code_id.sd_percentage', store=True)
    vat_percentage = fields.Float(string="VAT (%)", related='product_template_id.hs_code_id.vat_percentage', store=True)
    total_tax = fields.Float(string="Total Tax", compute="_compute_total_tax", store=True)
    price_unit = fields.Float(string="Unit Price")
    product_uom_qty = fields.Float(string="Quantity")

    @api.depends('sd_percentage', 'vat_percentage', 'price_unit', 'product_uom_qty')
    def _compute_total_tax(self):
        for line in self:
            line.total_tax = (line.sd_percentage + line.vat_percentage) * line.price_unit * line.product_uom_qty
