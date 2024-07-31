from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_type = fields.Selection([
        ('local_registered', 'Local (Registered)'),
        ('local_unregistered', 'Local (Unregistered)'),
        ('export', 'Export')
    ], string="Sales Type", required=True)
    export_type = fields.Selection([
        ('direct', 'Direct'),
        ('deemed', 'Deemed')
    ], string="Export Type")
    shipping_address = fields.Char(string="Shipping Address")
    billing_address = fields.Char(string="Billing Address")
    vehicle_number = fields.Char(string="Vehicle Number")
    selling_branch = fields.Char(string="Selling Branch")
    customer_bin = fields.Char(string="Customer BIN")
    customer_nid = fields.Char(string="Customer NID")
    custom_house = fields.Char(string="Custom House")
    bill_of_export_no = fields.Char(string="Bill of Export No.")
    bill_of_export_date = fields.Date(string="Bill of Export Date")
    item_code = fields.Char(string="Item Code")

    amount_total_with_taxes = fields.Monetary(string="Total with Taxes", compute="_compute_amount_total_with_taxes",
                                              store=True)
    @api.depends('order_line')
    def _compute_amount_total_with_taxes(self):
        for order in self:
            # Calculate the total amount including taxes
            total = 0.0
            for line in order.order_line:
                total += line.price_subtotal + line.total_tax
            order.amount_total_with_taxes = total

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sd_percentage = fields.Float(string="SD (%)", related='product_id.product_tmpl_id.hs_code_id.sd_percentage', store=True)
    vat_percentage = fields.Float(string="VAT (%)", related='product_id.product_tmpl_id.hs_code_id.vat_percentage', store=True)
    total_tax = fields.Float(string="Total Tax", compute="_compute_total_tax", store=True)

    @api.depends('sd_percentage', 'vat_percentage', 'price_unit', 'product_uom_qty')
    def _compute_total_tax(self):
        for line in self:
            total_price_before_tax = line.price_unit * line.product_uom_qty
            sd_amount = total_price_before_tax * (line.sd_percentage / 100)
            vat_amount = total_price_before_tax * (line.vat_percentage / 100)
            line.total_tax = sd_amount + vat_amount
