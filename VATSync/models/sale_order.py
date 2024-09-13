from odoo import models, fields, api
from odoo.exceptions import UserError
import requests

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
    selling_branch = fields.Many2one('selling.branch', string='Selling Branch')
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

    def action_generate_mushak_pdf(self):
        """Button for 6.3 to get the Mushak PDF URL."""
        api_url = 'http://localhost:3000/api/v1/generate_mushak_pdf'
        user_api_key = self.env.user.api_key

        headers = {'X-API-KEY': user_api_key}
        data = {'sale_number': self.name}  # Assuming sale number is in 'name' field

        response = requests.get(api_url, headers=headers, params=data)

        if response.status_code == 200:
            response_data = response.json()
            pdf_url = response_data.get('url')

            if pdf_url:
                return {
                    'type': 'ir.actions.act_url',
                    'url': pdf_url,
                    'target': 'new'
                }
            else:
                raise UserError('No URL returned from API!')
        else:
            raise UserError('Failed to generate Mushak PDF!')

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
