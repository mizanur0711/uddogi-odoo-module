from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class DateRangeWizard(models.TransientModel):
    _name = 'date.range.wizard'
    _description = 'Date Range Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def process_data(self):
        """Send API request with notification URL for processing data between dates."""
        _logger.info("Starting data processing...")

        # Fetch API base URL from system parameters
        api_base_url = self.env['ir.config_parameter'].sudo().get_param('VATSync.api_base_url')
        if not api_base_url:
            _logger.error("API base URL is not configured in the settings.")
            raise UserError("API base URL is not configured in the settings.")

        _logger.info(f"API base URL: {api_base_url}")
        api_endpoint = f"{api_base_url}/api/v1/fetch_with_process"

        # Fetch the Odoo base URL dynamically from system parameters
        odoo_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if not odoo_base_url:
            _logger.error("Odoo base URL is not configured in the settings.")
            raise UserError("Odoo base URL is not configured in the settings.")

        _logger.info(f"Odoo base URL: {odoo_base_url}")

        # Get the user's API key
        user_api_key = self.env['ir.config_parameter'].sudo().get_param('VATSync.api_key')
        if not user_api_key:
            _logger.error("API key is not configured.")
            raise UserError("API key is not configured in the settings.")

        _logger.info(f"Using API key: {user_api_key}")

        # Derive notification URL using the dynamically fetched Odoo base URL
        notification_url = f"{odoo_base_url}/api/v1/receive_status"
        _logger.info(f"Notification URL: {notification_url}")

        headers = {
            'Authorization': f'Bearer {user_api_key}',  # Assuming Bearer token authentication
            'Content-Type': 'application/json'
        }

        payload = {
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'webhook_odoo_url': notification_url
        }

        _logger.info(f"Sending request to {api_endpoint} with payload: {payload}")

        try:
            response = requests.post(api_endpoint, headers=headers, json=payload)
            _logger.info(f"Response status: {response.status_code}")
            _logger.info(f"Response text: {response.text}")
        except requests.exceptions.RequestException as e:
            _logger.error(f"Request failed: {str(e)}")
            raise UserError(f"Request failed: {str(e)}")

        if response.status_code == 500:  # Handle server error
            _logger.error("Server not responding (500 Internal Server Error).")
            return [{
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'Server not responding. Please try again later.',
                    'type': 'danger',
                    'sticky': False,
                },
            }, {
                'type': 'ir.actions.act_window_close',  # This closes the wizard window
            }]
        elif response.status_code in [200, 204]:  # Handle both 200 and 204 as success
            return [{
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Data processing initiated successfully.',
                    'type': 'success',
                    'sticky': False,
                },
            }, {
                'type': 'ir.actions.act_window_close',  # This closes the wizard window
            }]
        else:
            _logger.error(f"Failed to process data! Status: {response.status_code} - {response.text}")
            raise UserError(f'Failed to process data! Status: {response.status_code}')
