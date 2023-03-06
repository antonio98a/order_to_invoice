# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    orders = fields.Char("Orders")
    mark = fields.Char("Mark")
    