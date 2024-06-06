# models/res_company_extended.py
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    business_partner_bin = fields.Char(string="BIN No.")
    business_partner_origin = fields.Selection([
        ('import', 'Import'),
        ('export', 'Export'),
        ('import_export', 'Import and Export'),
        ('local', 'Local'),
        ('local_overseas', 'Local & Overseas')
    ], string="Business Type")

    business_partner_ownership = fields.Selection([
        ('private_limited', 'Private Limited'),
        ('partnership', 'Partnership'),
        ('public_limited', 'Public Limited'),
        ('proprietorship', 'Proprietorship'),
        ('others', 'Others')
    ], string="Type of Ownership")
