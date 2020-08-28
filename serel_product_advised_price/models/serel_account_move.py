# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    show_in_report = fields.Boolean(string='Show in Report', default=True)
    qty_integer = fields.Integer(string='Quantity in Integer', compute='_compute_qty_integer', store=True)

    @api.depends('quantity')
    def _compute_qty_integer(self):
        for line in self:
            line.qty_integer = int(line.quantity)
            if line.qty_integer != line.quantity:
                line.qty_integer = False
