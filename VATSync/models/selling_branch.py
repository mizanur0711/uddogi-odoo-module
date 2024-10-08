from odoo import models, fields

class SellingBranch(models.Model):
    _name = 'selling.branch'
    _description = 'Selling Branch'

    branch_id = fields.Char(string='Branch ID')
    name = fields.Char(string='Branch Name', required=True)
    address = fields.Char(string='Address')
    active = fields.Boolean(string='Active', default=True)
