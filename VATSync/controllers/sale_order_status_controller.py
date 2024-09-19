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

        # Store the notification in the notification.message model
        notification = request.env['notification.message'].sudo().create({
            'name': 'Notification',
            'message': message,
            'notification_type': 'success' if status else 'error'
        })

        # Create an activity based on the notification
        request.env['mail.activity'].sudo().create({
            'activity_type_id': request.env.ref('mail.mail_activity_data_todo').id,
            'res_id': request.env.user.partner_id.id,
            'res_model_id': request.env.ref('base.model_res_partner').id,
            'summary': notification.name,
            'note': notification.message,
            'date_deadline': fields.Date.today()  # Set a deadline for the activity
        })

        return {
            'status': 'success',
            'message': 'Notification message stored and activity created successfully.'
        }
