from odoo import http
from odoo.http import request


class MyController(http.Controller):

    @http.route('/uddogi_odoo_module/hello', type='http', auth='none', methods=['GET'], csrf=False)
    def hello(self):
        return "hello for now"
