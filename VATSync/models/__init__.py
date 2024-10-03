from . import sale_order
from . import product_info
from . import res_partner_extended
from . import hs_code
from . import selling_branch
from . import res_config_settings
from . import message_notification_vms
from odoo import api, SUPERUSER_ID

def start_vat_tour(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.module.module'].search([('name', '=', 'VATSync')]).write({'state': 'to upgrade'})
    env['ir.module.module'].upgrade_module(['VATSync'])
