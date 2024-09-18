from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_base_url = fields.Char(
        string="API Base URL",
        config_parameter='VATSync.api_base_url',
        help="Base URL for external API calls"
    )

    api_key = fields.Char(
        string="Global API Key",
        config_parameter='VATSync.api_key',
        help="Global API Key for VATSync integration"
    )

    def generate_api_key(self):
        # Logic to generate a new API key
        import uuid
        new_key = str(uuid.uuid4())
        self.env['ir.config_parameter'].sudo().set_param('VATSync.api_key', new_key)

        # Return an action to show a notification
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f"New API key generated: {new_key}",
                'sticky': False,
            }
        }
