# models/res_config_settings.py
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_base_url = fields.Char(
        string="API Base URL",
        config_parameter='VATSync.api_base_url',  # This ensures it is saved in the settings
        help="Base URL for external API calls"
    )
