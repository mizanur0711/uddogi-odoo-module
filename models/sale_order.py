# models/sale_order.py
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    trans_number = fields.Char(string="Transaction Reference Number")
    challan_no = fields.Char(string="Challan Number")
    challan_date = fields.Date(string="Challan Date")
    entry_date = fields.Date(string="Entry Date")
    process_date = fields.Datetime(string="Process Date")
    remarks = fields.Text(string="Remarks")
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    hs_code_id = fields.Many2one('hs.code', string='HS Code')
    cd_percentage = fields.Float(string='CD (%)', related='hs_code_id.cd_percentage', readonly=True)
    sd_percentage = fields.Float(string='SD (%)', related='hs_code_id.sd_percentage', readonly=True)
    vat_percentage = fields.Float(string='VAT (%)', related='hs_code_id.vat_percentage', readonly=True)
    ait_percentage = fields.Float(string='AIT (%)', related='hs_code_id.ait_percentage', readonly=True)
    rd_percentage = fields.Float(string='RD (%)', related='hs_code_id.rd_percentage', readonly=True)
    at_percentage = fields.Float(string='AT (%)', related='hs_code_id.at_percentage', readonly=True)