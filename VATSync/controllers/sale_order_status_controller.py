import logging
from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)

class SaleOrderStatusController(http.Controller):

    @http.route('/api/v1/receive_status', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_status(self, **kwargs):
        _logger.info("Received request at /api/v1/receive_status")

        # Extract status and message from request payload
        status = request.jsonrequest.get('status')
        message = request.jsonrequest.get('message', 'No message provided')

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
        activity_type = self.env.ref('mail.mail_activity_data_todo').id

        # Create a general notification activity (not tied to any specific sale order)
        self.env['mail.activity'].create({
            'activity_type_id': activity_type,
            'res_id': False,  # No specific record id
            'res_model_id': False,  # No specific model id
            'summary': f"General Status Update: From UDDOGI",
            'note': f"Message: {message}",
            'user_id': self.env.user.id,
            'date_deadline': fields.Date.today(),
        })
