from odoo import http
from odoo.http import request
import json
import logging

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

        # Extracting status and message from the request body
        status = request_data.get('status')
        message = request_data.get('message', 'No message provided')

        _logger.info(f"Received status: {status}")
        _logger.info(f"Received message: {message}")

        token = request.httprequest.headers.get('Authorization')
        _logger.info(f"Received Authorization header: {token}")

        if not token or not token.startswith('Bearer '):
            _logger.error('Bearer token is required.')
            return {'error': 'Bearer token is required.'}

        bearer_token = token[len('Bearer '):]

        global_api_key = request.env['ir.config_parameter'].sudo().get_param('VATSync.api_key')
        _logger.info(f"Global API key from config: {global_api_key}")

        if bearer_token != global_api_key:
            _logger.error('Invalid Bearer token.')
            return {'error': 'Invalid Bearer token.'}

        try:
            # Convert boolean status to 'success' or 'error'
            notification_type = 'success' if status else 'error'

            # Call the notify_user method in sale.order model to trigger notification
            response = request.env['sale.order'].sudo().notify_user(message, status=notification_type)

            # Save the message to the notification.message model
            request.env['notification.message'].sudo().create({
                'name': 'Status Update',
                'message': message,
                'notification_type': notification_type,  # Either 'success' or 'error'
            })

            return response

        except Exception as e:
            # Save the error to the notification.message model
            request.env['notification.message'].sudo().create({
                'name': 'Error',
                'message': str(e),
                'notification_type': 'error',
            })

            return {'error': str(e)}
