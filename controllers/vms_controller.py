from odoo import http
from odoo.http import request
import json
from datetime import datetime


class VMSController(http.Controller):

    @http.route('/api/VMS/VMSLastProcessDate', type='http', auth='public', methods=['GET'], csrf=False)
    def vms_last_process_date(self):
        # Fetch the latest sale order based on creation date with elevated permissions
        sale_order = request.env['sale.order'].sudo().search([], order='create_date desc', limit=1)

        # Format the creation date to DD/MM/YYYY
        if sale_order:
            creation_date = sale_order.create_date.strftime('%d/%m/%Y')
            return request.make_response(creation_date, headers=[('Content-Type', 'text/plain')])
        else:
            return request.make_response('No Sales Found', headers=[('Content-Type', 'text/plain')])

    @http.route('/api/VMS/GetVMSTranDataCount', type='http', auth='public', methods=['GET'], csrf=False)
    def get_vms_tran_data_count(self, StartDate=None, EndDate=None):
        if StartDate and EndDate:
            try:
                # Convert the date format from dd/mm/yyyy to yyyy-mm-dd using datetime
                start_date = datetime.strptime(StartDate, '%d/%m/%Y').strftime('%Y-%m-%d')
                end_date = datetime.strptime(EndDate, '%d/%m/%Y').strftime('%Y-%m-%d')

                # Fetch sales orders within the date range and with 'sale' state
                sale_orders = request.env['sale.order'].sudo().search([
                    ('date_order', '>=', start_date),
                    ('date_order', '<=', end_date),
                    ('state', '=', 'sale')
                ])

                # Return the count of sales orders as a JSON response
                return request.make_response(str(len(sale_orders)), headers=[('Content-Type', 'application/json')])

            except ValueError:
                return "Invalid date format. Please provide StartDate and EndDate in the format dd/mm/yyyy."
        else:
            return "StartDate and EndDate parameters are required."

    @http.route('/api/VMS/GetVMSTranData', type='http', auth='public', methods=['GET'], csrf=False)
    def get_vms_tran_data(self, StartDate=None, EndDate=None, pageSize=10, pageNo=0):
        try:
            # Validate and parse input dates
            if not StartDate or not EndDate:
                return request.make_response(
                    json.dumps({'error': 'StartDate and EndDate are required'}),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )

            start_date = datetime.strptime(StartDate, '%d/%m/%Y').strftime('%Y-%m-%d')
            end_date = datetime.strptime(EndDate, '%d/%m/%Y').strftime('%Y-%m-%d')

            # Fetch sale orders within the date range and with status 'sale'
            sale_orders = request.env['sale.order'].sudo().search([
                ('date_order', '>=', start_date),
                ('date_order', '<=', end_date),
                ('state', '=', 'sale')
            ])

            # Initialize response data list and handle pagination
            response_data = []
            start = int(pageNo) * int(pageSize)
            end = start + int(pageSize)

            for order in sale_orders[start:end]:
                for line in order.order_line:
                    item_data = {
                        "number": order.id,
                        "trans_number": order.name,
                        "challan_date": order.date_order.strftime('%Y-%m-%dT%H:%M:%S'),
                        "entry_date": order.create_date.strftime('%Y-%m-%dT%H:%M:%S'),
                        "challan_no": order.name,
                        "BranchId": 1,  # Replace with actual branch ID logic
                        "trans_reg_status": "Unregistered",  # Adjust based on actual logic
                        "branch_name": "Navana Foods Central Warehouse",  # Replace with actual branch name
                        "branch_address": "220 Kunipara ,Tejgoan I/A,Dhaka",  # Replace with actual branch address
                        "CounterBranchId": 21,  # Replace with actual counter branch ID logic
                        "trans_type": 18,  # Sales
                        "trans_type_name": "Sales",
                        "TranSide": 2,
                        "counter_branch_name": "NAVANA FOODS SUPPORT OFFICE",  # Replace with actual counter branch name
                        "counter_branch_address": "House # 2/B, Road #71, Gulshan-02, Dhaka-1212, Bangladesh",
                        # Replace with actual counter branch address
                        "business_partner_name": "NAVANA FOODS SUPPORT OFFICE",  # Replace with actual partner name
                        "business_partner_address": "House # 2/B, Road #71, Gulshan-02, Dhaka-1212, Bangladesh",
                        # Replace with actual partner address
                        "business_partner_reg_status": False,
                        "business_partner_bin": "N/A",
                        "business_partner_nid": "N/A",
                        "SKUType": 1,
                        "item_hs_code": line.product_id.default_code,
                        "item_name": line.product_id.name,
                        "item_classification": "Product",
                        "item_inventory_method": "FIFO",
                        "item_nature": "Exempted",
                        "item_unit_of_measurement_name": line.product_uom.name,
                        "item_unit_of_measurement_code": line.product_uom.name,
                        "item_quantity": line.product_uom_qty,
                        "item_unit_price": line.price_unit,
                        "TradePrice": 130.0,  # Adjust based on actual logic
                        "BatchPrice": line.price_unit,
                        "item_tran_value": line.price_subtotal,
                        "ImpactQty": -line.product_uom_qty,
                        "ImpactValue": -line.price_subtotal,
                        "item_sd_pc": line.sd_percentage,
                        "item_total_sd": line.sd_percentage * line.price_unit * line.product_uom_qty / 100,
                        "item_vat_pc": line.vat_percentage,
                        "item_total_vat": line.vat_percentage * line.price_unit * line.product_uom_qty / 100,
                        "item_total_tax": line.total_tax,
                        "AdditionalQty": 0.0,
                        "AdditionalTranValue": 0.0,
                        "AdditionalTranValueQty": 0.0,
                        "ProcessDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                        "remarks": "",
                        "ConversionValue": 1000.0,
                        "RefNo": "",
                        "vehicle_number": "Dhaka Metro-Sha-11-2026-Chiller Van",  # Replace with actual vehicle number
                        "GroupStamp": "N/A",
                        "SCAmount": 0.0,
                        "SortOrder": 18,
                        "business_partner_origin": "Local",
                        "business_partner_ownership": "Organization",
                        "business_partner_billing_address": "",
                        "business_partner_email": "N/A",
                        "transport_nature": "N/A",
                        "c_and_f_agent_name": "N/A",
                        "commercial_or_proforma_invoice_no": "N/A",
                        "boe_no": order.name,
                        "boe_date": order.date_order.strftime('%Y-%m-%dT%H:%M:%S'),
                        "customs_house": "Dhaka Custom house",
                        "lc_no": order.name,
                        "lc_date": order.date_order.strftime('%Y-%m-%dT%H:%M:%S'),
                        "item_av": 0.0,
                        "item_cd_pc": 0.0,
                        "item_total_cd": 0.0,
                        "item_rd_pc": 0.0,
                        "item_total_rd": 0.0,
                        "item_ait_pc": 0.0,
                        "item_total_ait": 0.0,
                        "item_at_pc": 0.0,
                        "item_total_at": 0.0,
                        "item_fixed_vat_amount_per_unit": 0.0,
                        "customs_station": "N/A",
                        "origin": "N/A",
                        "country_of_import": "N/A"
                    }
                    response_data.append(item_data)

            return request.make_response(
                json.dumps(response_data),
                headers={'Content-Type': 'application/json'},
                status=200
            )

        except ValueError:
            return request.make_response(
                json.dumps({'error': 'Invalid date format. Please use dd/mm/yyyy.'}),
                headers={'Content-Type': 'application/json'},
                status=400
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=500
            )