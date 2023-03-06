# -*- coding: utf-8 -*-


from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ReferralOrder(models.Model):
    _name="referral.order"
    _inherit= "mail.thread"

    name=fields.Char(
        "Order Name",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    folio = fields.Char(
        "Folio",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    date_order = fields.Date(
        "Date",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    registration = fields.Char(
        "Registration",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    patient = fields.Char(
        "Patient",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    document_class = fields.Selection(
        [('one','1'),('two','2'),('three','3')], 
        "Class",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    doctor = fields.Char(
        "Doctor",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    code = fields.Char(
        "Code",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    product_referral_ids = fields.One2many(
        "product.referral",
        "order_id",
        "Products",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    observations = fields.Text(
        "Observations",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    quant = fields.Integer(
        "Quantity",
        readonly=True,
        states = {"new": [("readonly", False)]}
    )
    state = fields.Selection([('new','No Facturada'),('completed','Facturada')], "state",
            default="new",
            required=True,
            readonly=True,
            copy=False,)
    
    invoice_id = fields.Many2one(
        "account.move",
        "Invoice",
        readonly=True,)

    def create_invoice(self):
        
        # A dictionary is created to store the product id and quantity
        product_values = {}
        # A dictionary is created to store the product id and folio order
        product_orders = {}
        #Validation to avoid duplicating orders already invoiced
        if any(order.state == "completed" for order in self):
            raise ValidationError(
                _(
                    "You cannot create invoice for remittance orders that have already been completed"
                ),
            )
        # Create the invoice and assign values to it.
        invoice_vals = {
            "move_type": "out_invoice",
            "invoice_date": fields.Date.today(),
        }
        invoice_obj = self.env["account.move"].sudo().create(invoice_vals)
        for order in self:
            for line in order.product_referral_ids:
                if line.product_id.id not in product_values:
                    product_values[line.product_id.id] = line.quant
                    product_orders[line.product_id.id] = order.folio
                else:
                    suma = (
                        product_values.get(line.product_id.id)
                        + line.quant
                    )
                    order_list = (product_orders.get(line.product_id.id)
                    + "," + order.folio)
                    product_values[line.product_id.id] = suma
                    product_orders[line.product_id.id] = order_list
            order.write({"state": "completed"})
            order.write({"invoice_id": invoice_obj.id}) 
        for clave in product_values:
            product_obj = self.env["product.product"].browse(clave)
            invoice_lines_vals ={
                "product_id": product_obj.id,
                "quantity": product_values[clave],
                "price_unit": product_obj.list_price,
                "mark": product_obj.x_studio_marca_1,
                "move_id": invoice_obj.id,
                "account_id": product_obj.property_account_income_id.id,
                "orders": product_orders[clave]
            }
            invoice_line_obj = self.env["account.move.line"].sudo().create(invoice_lines_vals)
        
        return {
            "view_type": "form",
            "view_mode": "form,tree",
            "res_model": "account.move",
            "res_id": invoice_obj.id,
            "view_id": False,
            "type": "ir.actions.act_window",
        }