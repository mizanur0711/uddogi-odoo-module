from odoo import models, fields, http
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
            with request.env.cr.savepoint():
                # Store the notification in the notification.message model (preferred approach)
                # Uncomment the following lines if using `message_post` is possible
                # notification = request.env['notification.message'].sudo().create({
                #     'name': 'Status Update Notification',
                #     'message': message,
                #     'notification_type': 'success' if status else 'error'
                # })
                # _logger.info(f"Notification created: {notification.id}")

                # **Temporary workaround (use with caution):**
                # Use `message_post` if possible, this is a less risky approach.
                # If `message_post` is not compatible with your Odoo version or there
                # are conflicts, uncomment the following lines to use a direct
                # database query.
                request.env.cr.execute(
                    """
                    INSERT INTO notification.message (name, message, notification_type)
                    VALUES ('Status Update Notification', %s, %s)
                    RETURNING id;
                    """,
                    (message, 'success' if status else 'error')
                )
                notification_id = request.env.cr.fetchone()[0]
                _logger.info(f"Notification (via direct query) created: {notification_id}")

                # Get all active users
                active_users = request.env['res.users'].sudo().search([('active', '=', True)])

                # Create an activity for each active user
                activity_type_id = request.env.ref('mail.mail_activity_data_todo').id
                model_id = request.env.ref('base.model_res_users').id

                for user in active_users:
                    activity = request.env['mail.activity'].sudo().create({
                        'activity_type_id': activity_type_id,
                        'res_id': user.id,
                        'res_model_id': model_id,
                        'user_id': user.id,
                        'summary': 'Status Update Notification',
                        'note': f"Status: {'Success' if status else 'Error'}\n\nMessage: {message}",
                        'date_deadline': fields.Date.today()
                    })
                    _logger.info(f"Activity created for user {user.name}: {activity.id}")

                    # Commented out as `message_post` is the preferred method
                    # user.sudo().message_notify(
                    #     body=f"Status Update: {message}",
                    #     message_type='notification',
                    #     subtype_xmlid='mail.mt_note',
                    # )
                    # _logger.info(f"Message posted to user's chatter: {user.name}")

                # Commit the transaction
                request.env.cr.commit()

        except Exception as e:
            _logger.error(f"Error processing notification and activities: {str(e)}")
            return {'error': f'Error processing notification and activities: {str(e)}'}

        return {}