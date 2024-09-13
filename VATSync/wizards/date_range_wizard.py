from odoo import models, fields, api
from odoo.exceptions import UserError
import requests


class DateRangeWizard(models.TransientModel):
    _name = 'date.range.wizard'
    _description = 'Date Range Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def process_data(self):
        """Send API request with notification URL for processing data between dates."""
        # Fetch API base URL from system parameters
        api_base_url = self.env['ir.config_parameter'].sudo().get_param('VATSync.api_base_url')
        if not api_base_url:
            raise UserError("API base URL is not configured in the settings.")
        api_endpoint = f"{api_base_url}/api/v1/is_new_data_available_on_odoo"

        # Fetch the Odoo base URL dynamically from system parameters
        odoo_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if not odoo_base_url:
            raise UserError("Odoo base URL is not configured in the settings.")

        # Get the user's API key
        user_api_key = self.env.user.api_key_ids[0].key

        # Derive notification URL using the dynamically fetched Odoo base URL
        notification_url = f"{odoo_base_url}/api/v1/receive_status"

        headers = {
            'Authorization': f'Bearer {user_api_key}'  # Assuming Bearer token authentication
        }

        params = {
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'notification_url': notification_url
        }

        response = requests.get(api_endpoint, headers=headers, params=params)

        if response.status_code == 200:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Data processing initiated successfully.',
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            raise UserError('Failed to process data!')
