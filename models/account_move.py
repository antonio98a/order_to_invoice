# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountMoveLine(models.Model):
    _inherit = "account.move"

    contract = fields.Char("Contract")
    period = fields.Char("Period")
    