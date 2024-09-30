from odoo import models, fields

class VatBangladeshWizard(models.TransientModel):
    _name = 'vat.bangladesh.wizard'
    _description = 'Vat Bangladesh Information'

    message = fields.Text(string='Message', default='This is the VAT information for Bangladesh.')

    def action_show_message(self):
        return {
            'name': 'VAT Bangladesh Info',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'vat.bangladesh.wizard',
            'target': 'new',
            'res_id': self.id,
        }
