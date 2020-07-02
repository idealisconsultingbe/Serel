# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelSaelOrderLine(models.Model):
    _inherit = 'sale.order.line'

    advised_sale_price = fields.Float('Advised Sale Price', digits='Product Price',
                                      related='product_id.pr_advised_sale_price')
    show_in_report = fields.Boolean(string='Show in Report', default=True)
    qty_integer = fields.Integer(string='Quantity in Integer', compute='_compute_qty_integer', store=True)

    @api.depends('product_uom_qty')
    def _compute_qty_integer(self):
        for line in self:
            line.qty_integer = int(line.product_uom_qty)
            if line.qty_integer != line.product_uom_qty:
                line.qty_integer = False
