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
    total_tax = fields.Float(string="Total Tax", compute="_compute_total_tax")

    cloned_order_line_ids = fields.One2many(
        'sale.order.line.clone',
        'order_id',
        string="Cloned Order Lines"
    )

    @api.depends('order_line.sd_percentage', 'order_line.vat_percentage', 'order_line.price_unit', 'order_line.product_uom_qty')
    def _compute_total_tax(self):
        for order in self:
            total_tax = 0.0
            for line in order.order_line:
                if order.sales_type != 'export':
                    total_tax += (line.sd_percentage + line.vat_percentage) * line.price_unit * line.product_uom_qty
            order.total_tax = total_tax

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sd_percentage = fields.Float(string="SD (%)", related='product_id.hs_code_id.sd_percentage', store=True)
    vat_percentage = fields.Float(string="VAT (%)", related='product_id.hs_code_id.vat_percentage', store=True)
    total_tax = fields.Float(string="Total Tax", compute="_compute_total_tax", store=True)

    @api.depends('sd_percentage', 'vat_percentage', 'price_unit', 'product_uom_qty')
    def _compute_total_tax(self):
        for line in self:
            line.total_tax = (line.sd_percentage + line.vat_percentage) * line.price_unit * line.product_uom_qty
