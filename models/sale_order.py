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
