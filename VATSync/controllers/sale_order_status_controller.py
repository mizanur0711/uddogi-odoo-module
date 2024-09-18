import logging
import json
from odoo import http, fields
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

        # Create a general notification activity
        self.create_general_notification_activity(
            status=status,
            message=message
        )

        _logger.info("Notification activity created successfully.")
        # Return a success response
        return {}

    def create_general_notification_activity(self, status, message):
        """Create a general notification activity."""
        activity_type = request.env.ref('mail.mail_activity_data_todo').id

        # Provide a default model ID (you can choose a model that is unlikely to cause issues)
        default_model_id = request.env.ref('base.model_res_users').id

        # Create a general notification activity (using sudo to bypass ACL restrictions)
        request.env['mail.activity'].sudo().create({
            'activity_type_id': activity_type,
            'res_id': 0,  # No specific record id
            'res_model_id': default_model_id,  # Provide a default or placeholder model ID
            'summary': f"General Status Update: From UDDOGI",
            'note': f"Message: {message}",
            'user_id': request.env.user.id,
            'date_deadline': fields.Date.today(),
        })
