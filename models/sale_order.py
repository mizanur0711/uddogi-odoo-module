# sale_order.py
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

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_sd_percentage = fields.Float(string="Total SD (%)", compute="_compute_total_sd_percentage")
    total_vat_percentage = fields.Float(string="Total VAT (%)", compute="_compute_total_vat_percentage")
    total_amount_with_tax = fields.Float(string="Total Amount with Tax", compute="_compute_total_amount_with_tax")

    @api.depends('order_line.sd_percentage', 'order_line.product_uom_qty')
    def _compute_total_sd_percentage(self):
        for order in self:
            order.total_sd_percentage = sum(line.sd_percentage * line.product_uom_qty for line in order.order_line)

    @api.depends('order_line.vat_percentage', 'order_line.product_uom_qty')
    def _compute_total_vat_percentage(self):
        for order in self:
            order.total_vat_percentage = sum(line.vat_percentage * line.product_uom_qty for line in order.order_line)

    @api.depends('order_line.total_tax')
    def _compute_total_amount_with_tax(self):
        for order in self:
            order.total_amount_with_tax = sum(line.total_tax for line in order.order_line)
