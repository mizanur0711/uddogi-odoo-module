import base64
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
        """Button for 6.3 to get the Mushak PDF URL and retrieve the PDF."""

        # Dynamically fetch the API base URL from system parameters
        api_base_url = self.env['ir.config_parameter'].sudo().get_param('VATSync.api_base_url')
        if not api_base_url:
            raise UserError("Mushak API base URL is not configured in the settings.")

        # Complete API URL for PDF generation
        api_url = f"{api_base_url}/api/v1/generate_mushak_pdf"

        # Fetch the user's API key (can be stored in config parameters)
        user_api_key = self.env['ir.config_parameter'].sudo().get_param('VATSync.api_key')
        if not user_api_key:
            raise UserError("Mushak API key is not configured in the settings.")

        # Set the headers with Bearer token and JSON content type
        headers = {
            'Authorization': f'Bearer {user_api_key}',
            'Content-Type': 'application/json'
        }

        # Prepare the data (assuming sale number is stored in 'name' field)
        data = {'sale_number': self.name}

        # Create a session to maintain authorization across requests
        session = requests.Session()
        session.headers.update(headers)

        try:
            # First request: Get the PDF URL
            response = session.get(api_url, json=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            try:
                response_data = response.json()
            except ValueError:
                raise UserError("Failed to decode JSON response from the Mushak API!")

            pdf_url = response_data.get('m_6_3_url')
            if not pdf_url:
                raise UserError("No URL returned from the Mushak API!")

            # Ensure the PDF URL is valid
            if not pdf_url.startswith('http'):
                raise UserError("Invalid URL received from the Mushak API!")

            # Second request: Get the PDF content
            pdf_response = session.get(pdf_url)
            pdf_response.raise_for_status()

            # Check if the content type is PDF
            if 'application/pdf' not in pdf_response.headers.get('Content-Type', ''):
                raise UserError("The URL did not return a PDF file.")

            # Generate a unique filename, ensure it's safe
            filename = f"mushak_6_3_{self.name.replace('/', '_')}.pdf"

            # Save the PDF content to a temporary file as attachment
            pdf_content = pdf_response.content
            attachment = self.env['ir.attachment'].create({
                'name': filename,
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': self._name,
                'res_id': self.id,
                'mimetype': 'application/pdf'
            })

            # Return an action to download the PDF
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}/{filename}?download=true',
                'target': 'self',
            }

        except requests.exceptions.RequestException as e:
            raise UserError(f"API request failed: {str(e)}")

        finally:
            session.close()


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
