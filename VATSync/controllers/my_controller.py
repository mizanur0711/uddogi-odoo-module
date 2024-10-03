from odoo import http
from odoo.http import request

class VATSyncController(http.Controller):
    @http.route('/vatsync/tour', auth='user', type='json')
    def start_tour(self):
        request.env['web_tour.tour']._tour_ensure_started('vat_bangladesh_tour')
