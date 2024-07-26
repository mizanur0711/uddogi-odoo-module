from odoo import http
from odoo.http import request
from datetime import datetime


class VMSController(http.Controller):

    @http.route('/api/vms/data_count', type='json', auth='public', methods=['GET'])
    def get_data_count(self, start_date, end_date):
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')

        # Query the database for the count of transactions
        transaction_count = request.env['your.transaction.model'].sudo().search_count([
            ('transaction_date', '>=', start_date),
            ('transaction_date', '<=', end_date)
        ])

        return {'data_count': transaction_count}

    @http.route('/api/vms/transactions', type='json', auth='public', methods=['GET'])
    def get_transactions(self, start_date, end_date, page_size=10, page_no=0):
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')

        # Calculate offset for pagination
        offset = page_no * page_size

        # Query the database for transactions
        transactions = request.env['your.transaction.model'].sudo().search([
            ('transaction_date', '>=', stfrom odoo import http
            from odoo.http import request
            from datetime import datetime


class VMSController(http.Controller):

    @http.route('/api/vms/data_count', type='json', auth='public', methods=['GET'])
    def get_data_count(self, start_date, end_date):
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')

        # Query the database for the count of transactions
        transaction_count = request.env['your.transaction.model'].sudo().search_count([
            ('transaction_date', '>=', start_date),
            ('transaction_date', '<=', end_date)
        ])

        return {'data_count': transaction_count}

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

    @http.route('/api/vms/last_processed_date', type='json', auth='public', methods=['GET'])
    def get_last_processed_date(self):
        # Get the last processed date from the database
        last_transaction = request.env['your.transaction.model'].sudo().search([], order='transaction_date desc',
                                                                               limit=1)
        if last_transaction:
            last_processed_date = last_transaction.transaction_date.strftime('%d/%m/%Y')
        else:
            last_processed_date = None

        return {'last_processed_date': last_processed_date}


art_date),
('transaction_date', '<=', end_date)
], limit = page_size, offset = offset)

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


@http.route('/api/vms/last_processed_date', type='json', auth='public', methods=['GET'])
def get_last_processed_date(self):
    # Get the last processed date from the database
    last_transaction = request.env['your.transaction.model'].sudo().search([], order='transaction_date desc',
                                                                           limit=1)
    if last_transaction:
        last_processed_date = last_transaction.transaction_date.strftime('%d/%m/%Y')
    else:
        last_processed_date = None

    return {'last_processed_date': last_processed_date}
