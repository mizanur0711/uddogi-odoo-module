from odoo import http
from odoo.exceptions import UserError
from odoo.http import request
import json
import logging
import requests as rqs

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
            # Call the notify_user method in sale.order model to trigger notification
            return request.env['sale.order'].sudo().notify_user(message, status)
        except Exception as e:
            _logger.error("Error sending notification: %s", e)
            return {'status': 'error', 'message': str(e)}

        # try:
        #     request.env['bus.bus']._sendone(
        #         'your_channel_name',  # Channel Name
        #         'notification',  # Notification Type
        #         {  # Message Payload
        #             'title': 'VAT Bangladesh Status Update',
        #             'message': message,
        #             'type': 'success' if status == 'success' else 'danger',
        #         }
        #     )
        # except Exception as e:
        #     _logger.error("Error sending notification: %s", e)
        #     return {'status': 'error', 'message': str(e)}

        # # Send notification
        # notification = {
        #     'title': 'VAT Bangladesh Status Update',
        #     'message': message,
        #     'type': 'success' if status == 'success' else 'danger',
        # }
        # base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # url = f"{base_url}/notify"
        # response = rqs.post(url, json=notification)
        #
        # if response.status_code != 200:
        #     _logger.error(f"Error sending notification: {response.text}")
        #
        # return {
        #     'status': status,
        #     'message': message,
        # }