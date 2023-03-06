# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductReferral(models.Model):
    _name = "product.referral"

    order_id = fields.Many2one("referral.order", "Order")
    product_id = fields.Many2one("product.product", "Product")
    product_observations = fields.Char("Observations")
    code = fields.Char("Code")
    catalog = fields.Char("Catalog")
    quant = fields.Float("Quantity")
    