# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelSaelOrderLine(models.Model):
    _inherit = 'sale.order.line'

    advised_sale_price = fields.Float('Advised Sale Price', digits='Product Price', related='product_id.pr_advised_sale_price')
