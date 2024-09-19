# message_notification_vms.py
from odoo import models, fields

class NotificationMessage(models.Model):
    _name = 'notification.message'
    _description = 'Notification Message'

    name = fields.Char(string='Title', required=True)
    message = fields.Text(string='Message', required=True)
    notification_type = fields.Selection([('success', 'Success'), ('error', 'Error')], string='Notification Type', required=True)
    active = fields.Boolean(string='Active', default=True)
