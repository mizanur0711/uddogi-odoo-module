from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)

class SaleOrderStatusController(http.Controller):

    @http.route('/api/v1/receive_status', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_status(self, **kwargs):
        _logger.info("Received request at /api/v1/receive_status")

        try:
            request_data = json.loads(request.httprequest.data.decode('utf-8'))
            _logger.info(f"Received JSON request body: {request_data}")
        except Exception as e:
            _logger.error(f"Error extracting JSON data: {str(e)}")
            return {'error': 'Invalid JSON payload'}

        status = request_data.get('status')
        message = request_data.get('message', 'No message provided')

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

        # Create an activity or notification in Odoo (on sale orders, or another model)
        model = request.env['sale.order']  # Change to your desired model
        orders = model.search([])  # Add filtering logic if needed

        for order in orders:
            order.activity_schedule(
                'mail.mail_activity_data_todo',  # Activity type
                user_id=order.user_id.id,  # Notify the responsible user
                note=f'{message}',  # Display the message from the webhook
            )

        return {'success': True, 'message': 'Notifications created successfully'}
