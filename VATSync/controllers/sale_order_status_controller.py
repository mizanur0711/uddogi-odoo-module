from odoo import http, fields
from odoo.http import request

class SaleOrderStatusController(http.Controller):

    @http.route('/api/v1/receive_status', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_status(self, **kwargs):
        # Extract status and message from request payload
        status = request.jsonrequest.get('status')
        message = request.jsonrequest.get('message', 'No message provided')

        # Extract Bearer token from headers
        token = request.httprequest.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return {'error': 'Bearer token is required.'}

        bearer_token = token[len('Bearer '):]

        # Validate the Bearer token
        if not self.validate_bearer_token(bearer_token):
            return {'error': 'Invalid Bearer token.'}

        # Create a general notification activity
        self.create_general_notification_activity(
            status=status,
            message=message
        )

        # Return an empty response to indicate success
        return {}

    def validate_bearer_token(self, token):
        """Validate the Bearer token with the global API key."""
        # Fetch the global API key from system parameters
        global_api_key = request.env['ir.config_parameter'].sudo().get_param('VATSync.api_key')

        # Compare the provided token with the global API key
        return token == global_api_key

    def create_general_notification_activity(self, status, message):
        """Create a general notification activity."""
        activity_type = self.env.ref('mail.mail_activity_data_todo').id

        # Create a general notification activity (not tied to any specific sale order)
        self.env['mail.activity'].create({
            'activity_type_id': activity_type,
            'res_id': False,  # No specific record id
            'res_model_id': False,  # No specific model id
            'summary': f"General Status Update: {status}",
            'note': f"Message: {message}",
            'user_id': self.env.user.id,
            'date_deadline': fields.Date.today(),
        })
