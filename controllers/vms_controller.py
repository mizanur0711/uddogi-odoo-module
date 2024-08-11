from odoo import http
from odoo.http import request
from datetime import datetime
class VMSController(http.Controller):

    @http.route('/api/VMS/VMSLastProcessDate', type='http', auth='public', methods=['GET'], csrf=False)
    def vms_last_process_date(self):
        # Fetch the latest sale order based on creation date
        sale_order = request.env['sale.order'].search([], order='create_date desc', limit=1)

        # Format the creation date to DD/MM/YYYY
        if sale_order:
            creation_date = sale_order.create_date.strftime('%d/%m/%Y')
        else:
            creation_date = 'No Sales Found'

        # Return the creation date as a plain text response
        return creation_date

    @http.route('/api/VMS/GetVMSTranDataCount', type='http', auth='public', methods=['GET'], csrf=False)
    def get_vms_tran_data_count(self, StartDate=None, EndDate=None):
        if StartDate and EndDate:
            # Convert the date format from dd/mm/yyyy to yyyy-mm-dd
            start_date = StartDate.split("/")[2] + "-" + StartDate.split("/")[1] + "-" + StartDate.split("/")[0]
            end_date = EndDate.split("/")[2] + "-" + EndDate.split("/")[1] + "-" + EndDate.split("/")[0]

            # Fetch sales orders within the date range
            sale_orders = request.env['sale.order'].sudo().search([
                ('date_order', '>=', start_date),
                ('date_order', '<=', end_date),
                ('state', '=', 'sale')
            ])

            # Return the count of sales orders
            return str(len(sale_orders))
        else:
            return "Invalid date format. Please provide StartDate and EndDate in the format dd/mm/yyyy."


    @http.route('/api/vms/transactions', type='json', auth='public', methods=['GET'])
    def get_transactions(self, start_date, end_date, page_size=10, page_no=0):
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')

        # Calculate offset for pagination
        offset = page_no * page_size

        # Query the database for transactions
        transactions = request.env['your.transaction.model'].sudo().search([
            ('transaction_date', '>=', start_date),
            ('transaction_date', '<=', end_date)
        ], limit=page_size, offset=offset)

        # Prepare transaction data
        transactions_data = []
        for transaction in transactions:
            transactions_data.append({
                'id': transaction.id,
                'date': transaction.transaction_date.strftime('%d/%m/%Y'),
                'time': transaction.transaction_date.strftime('%H:%M:%S'),
                # Add other fields as needed
            })

        return {'transactions': transactions_data}