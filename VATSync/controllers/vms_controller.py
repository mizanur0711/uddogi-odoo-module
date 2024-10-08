from odoo import http
from odoo.http import request
import json
from datetime import datetime


class VMSController(http.Controller):

    @http.route('/api/VMS/VMSLastProcessDate', type='http', auth='public', methods=['GET'], csrf=False)
    def vms_last_process_date(self):
        # Fetch the latest sale order based on creation date with elevated permissions
        sale_order = request.env['sale.order'].sudo().search([], order='create_date desc', limit=1)

        # Format the creation date to "YYYY-MM-DDTHH:MM:SS" and wrap it with double quotes
        if sale_order:
            creation_date = sale_order.create_date.strftime('%Y-%m-%dT%H:%M:%S')
            quoted_creation_date = f'"{creation_date}"'  # Wrap the date with double quotes
            return request.make_response(quoted_creation_date, headers={'Content-Type': 'text/plain'})
        else:
            return request.make_response('"No Sales Found"', headers={'Content-Type': 'text/plain'})

    @http.route('/api/VMS/GetVMSTranDataCount', type='http', auth='public', methods=['GET'], csrf=False)
    def get_vms_tran_data_count(self, StartDate=None, EndDate=None):
        if StartDate and EndDate:
            try:
                # Convert date format from "10 Aug 2024" to "YYYY-MM-DD"
                start_date = datetime.strptime(StartDate, '%d %b %Y').strftime('%Y-%m-%d')
                end_date = datetime.strptime(EndDate, '%d %b %Y').strftime('%Y-%m-%d')

                # Fetch sales orders within the date range and with 'sale' state
                sale_order_count = request.env['sale.order'].sudo().search_count([
                    ('create_date', '>=', start_date),
                    ('create_date', '<=', end_date),
                    ('state', '=', 'sale')
                ])

                # Return the count of sales orders as a plain text response
                return request.make_response(str(sale_order_count), headers={'Content-Type': 'text/plain'})

            except ValueError:
                return request.make_response(
                    json.dumps({'error': 'Invalid date format. Please provide StartDate and EndDate in the format "10 Aug 2024".'}),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )
        else:
            return request.make_response(
                json.dumps({'error': 'StartDate and EndDate parameters are required.'}),
                headers={'Content-Type': 'application/json'},
                status=400
            )

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

            # Convert date format from "10 Aug 2024" to "YYYY-MM-DD"
            start_date = datetime.strptime(StartDate, '%d %b %Y').strftime('%Y-%m-%d')
            end_date = datetime.strptime(EndDate, '%d %b %Y').strftime('%Y-%m-%d')

            # Fetch sale orders within the date range and with status 'sale'
            sale_orders = request.env['sale.order'].sudo().search([
                ('create_date', '>=', start_date),
                ('create_date', '<=', end_date),
                ('state', '=', 'sale')
            ], order='id asc')

            # Initialize response data list and handle pagination
            response_data = []
            start = int(pageNo) * int(pageSize)
            end = start + int(pageSize)

            for order in sale_orders[start:end]:
                # Fetch selling branch details
                selling_branch = order.selling_branch or False
                branch_id = selling_branch.branch_id if selling_branch else "N/A"
                branch_name = selling_branch.name if selling_branch else "N/A"
                branch_address = selling_branch.address if selling_branch else "N/A"

                # Fetch customer details
                customer = order.partner_id
                customer_name = customer.name or "N/A"
                customer_address = customer.contact_address or "N/A"

                # Determine registration status based on customer_bin
                trans_reg_status = "Registered" if order.customer_bin else "Unregistered"


                for line in order.order_line:
                    hs_code = line.product_id.hs_code_id
                    item_data = {
                        "number": order.id,
                        "trans_number": order.name,
                        "challan_date": order.date_order.strftime('%Y-%m-%dT%H:%M:%S'),
                        "entry_date": order.create_date.strftime('%Y-%m-%dT%H:%M:%S'),
                        "challan_no": order.name,
                        "BranchId": branch_id,
                        "trans_reg_status": trans_reg_status,
                        "branch_name": branch_name,
                        "branch_address": branch_address,
                        "CounterBranchId": branch_id,
                        "trans_type": 18,  # Sales
                        "trans_type_name": "Sales",
                        "TranSide": 2,
                        "counter_branch_name": branch_name,
                        "counter_branch_address": branch_address,
                        "business_partner_name": customer_name,
                        "business_partner_address": customer_address,
                        "business_partner_reg_status": trans_reg_status == "Registered",
                        "business_partner_bin": order.customer_bin or "N/A",
                        "business_partner_nid": order.customer_nid or "N/A",
                        "SKUType": 1,
                        "item_hs_code": hs_code.name,
                        "item_name": line.product_id.name,
                        "item_classification": "Product" if line.product_id.detailed_type == 'product' else "Service",
                        "item_inventory_method": (
                            "FIFO" if line.product_id.item_inventory_method == 'fifo' else
                            "LIFO" if line.product_id.item_inventory_method == 'lifo' else
                            "Average" if line.product_id.item_inventory_method == 'average' else "N/A"
                        ),
                        "item_nature": "Exempted",
                        "item_unit_of_measurement_name": line.product_uom.name,
                        "item_unit_of_measurement_code": line.product_uom.name,
                        "item_quantity": line.product_uom_qty,
                        "item_unit_price": line.product_id.standard_price,
                        "TradePrice": line.price_unit,
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
                        "vehicle_number": order.vehicle_number,  # Replace with actual vehicle number
                        "GroupStamp": "N/A",
                        "SCAmount": 0.0,
                        "SortOrder": 18,
                        "business_partner_origin": customer.business_partner_origin or "N/A",
                        "business_partner_ownership": customer.business_partner_ownership or "N/A",
                        "business_partner_billing_address": order.billing_address,
                        "business_partner_email": customer.email,
                        "transport_nature": "N/A",
                        "c_and_f_agent_name": "N/A",
                        "commercial_or_proforma_invoice_no": "N/A",
                        "boe_no": order.bill_of_export_no or "N/A",
                        "boe_date": order.bill_of_export_date.strftime('%Y-%m-%dT%H:%M:%S') if order.bill_of_export_date else "N/A",
                        "customs_house": order.custom_house or "N/A",
                        "lc_no": order.name,
                        "lc_date": order.date_order.strftime('%Y-%m-%dT%H:%M:%S') if order.date_order else "N/A",
                        "item_av": line.price_subtotal,
                        "item_cd_pc": hs_code.cd_percentage if hs_code else 0.0,
                        "item_total_cd": hs_code.cd_percentage * line.price_unit * line.product_uom_qty / 100 if hs_code else 0.0,
                        "item_rd_pc": hs_code.rd_percentage if hs_code else 0.0,
                        "item_total_rd": hs_code.rd_percentage * line.price_unit * line.product_uom_qty / 100 if hs_code else 0.0,
                        "item_ait_pc": hs_code.ait_percentage if hs_code else 0.0,
                        "item_total_ait": hs_code.ait_percentage * line.price_unit * line.product_uom_qty / 100 if hs_code else 0.0,
                        "item_at_pc": hs_code.at_percentage if hs_code else 0.0,
                        "item_total_at": hs_code.at_percentage * line.price_unit * line.product_uom_qty / 100 if hs_code else 0.0,
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