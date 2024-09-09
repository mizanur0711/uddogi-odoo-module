from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_base_url = fields.Char(string="API Base URL", config_parameter='VATSync.api_base_url', help="Base URL for external API calls")
