import logging
import json
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class SaleOrderStatusController(http.Controller):

    @http.route('/api/v1/receive_status', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_status(self, **kwargs):
        _logger.info("Received request at /api/v1/receive_status")

        try:
            # Convert raw byte data to a string and parse it into a Python dictionary
            request_data = json.loads(request.httprequest.data.decode('utf-8'))
            _logger.info(f"Received JSON request body: {request_data}")
        except Exception as e:
            _logger.error(f"Error extracting JSON data: {str(e)}")
            return {'error': 'Invalid JSON payload'}

        # Extract status and message from request payload
        status = request_data.get('status')
        message = request_data.get('message', 'No message provided')

        _logger.info(f"Received status: {status}")
        _logger.info(f"Received message: {message}")

        # Extract Bearer token from headers
        token = request.httprequest.headers.get('Authorization')
        _logger.info(f"Received Authorization header: {token}")

        if not token or not token.startswith('Bearer '):
            _logger.error('Bearer token is required.')
            return {'error': 'Bearer token is required.'}

        bearer_token = token[len('Bearer '):]

        # Fetch the global API key from system parameters
        global_api_key = request.env['ir.config_parameter'].sudo().get_param('VATSync.api_key')
        _logger.info(f"Global API key from config: {global_api_key}")

        # Validate the Bearer token
        if bearer_token != global_api_key:
            _logger.error('Invalid Bearer token.')
            return {'error': 'Invalid Bearer token.'}

        # Determine notification type based on status
        if status:
            notification_type = 'success'
            title = 'Success'
        else:
            notification_type = 'danger'
            title = 'Error'

        # Display a notification with the message from the request
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,  # Use message from the request payload
                'type': notification_type,
                'sticky': False,
            }
        }
