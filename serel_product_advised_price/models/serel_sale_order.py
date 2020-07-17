# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    advised_sale_price = fields.Float('Advised Sale Price', digits='Product Price',
                                      related='product_id.pr_advised_sale_price')
    show_in_report = fields.Boolean(string='Show in Report', default=True)
    show_in_report_section = fields.Boolean(string='Show in Report Section')

    qty_integer = fields.Integer(string='Quantity in Integer', compute='_compute_qty_integer', store=True)

    @api.depends('product_uom_qty')
    def _compute_qty_integer(self):
        for line in self:
            line.qty_integer = int(line.product_uom_qty)
            if line.qty_integer != line.product_uom_qty:
                line.qty_integer = False

    @api.onchange('show_in_report')
    def _onchange_show_in_report_section(self):
        for line in self:
            for so_line in line.order_id.order_line:
                if so_line.display_type == 'line_section' and so_line.display_name == line.display_name:
                    line.show_in_report_section = so_line.show_in_report
                else:
                    line.show_in_report_section = True  # TO CHANGE
