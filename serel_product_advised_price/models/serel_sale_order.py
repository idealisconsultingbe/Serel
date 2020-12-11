# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelSaleOrderLine(models.Model):
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

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        res = super(SerelSaleOrderLine, self)._action_launch_stock_rule(previous_product_uom_qty=previous_product_uom_qty)
        orders = list(set(x.order_id for x in self))
        for order in orders:
            reassign = order.picking_ids.filtered(lambda x: x.state=='confirmed' or (x.state in ['waiting', 'assigned'] and not x.printed))
            if reassign:
                reassign.action_assign()
                move_lines = reassign.move_lines.filtered(lambda x: x.bom_line_id.bom_id.type != 'phantom')
                so_lines = self.filtered(lambda x: not x.display_type and x.product_id.type != 'service')
                if so_lines:
                    i = 0
                    for line in move_lines:
                        line.description_picking = so_lines[i].name
                        i += 1
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tag_ids = fields.Many2many('res.partner.category', column1='order_id', column2='category_id', string='Tags')
    serel_order_date = fields.Date(string='Order Date')
    date_order = fields.Date(string='Serel Confirm Date')

