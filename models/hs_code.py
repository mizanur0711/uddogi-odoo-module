from odoo import models, fields

class HSCode(models.Model):
    _name = 'hs.code'
    _description = 'HS Code'

    name = fields.Char(string='HS Code', required=True)
    fiscal_year = fields.Char(string='Fiscal Year')
    description = fields.Text(string='Description')
    cd_percentage = fields.Float(string='CD (%)')
    sd_percentage = fields.Float(string='SD (%)')
    vat_percentage = fields.Float(string='VAT (%)')
    ait_percentage = fields.Float(string='AIT (%)')
    rd_percentage = fields.Float(string='RD (%)')
    at_percentage = fields.Float(string='AT (%)')
    active = fields.Boolean(string='Active', default=True)
