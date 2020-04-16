# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelProductTmpl(models.Model):
    _inherit = 'product.template'

    tag_product_ids = fields.Many2many('tag.product.template', 'product_template_tag_rel', 'product_id', 'tag_id', string='Tags')
    advised_sale_price = fields.Float(string='Advised Sale Price', digits='Product Price', compute='get_advised_price', store=True)
    default_code = fields.Char(required=True)

    _sql_constraints = [
        ('unique_default_code', 'unique(default_code)', 'This reference already exists!')
    ]

    @api.depends('standard_price')
    def get_advised_price(self):
        """
        Set the advised price defined by the pricelist with the flag 'advised_pricelist' checked.
        """
        for product_tmpl in self:
            advised_price_pricelist = self.env['product.pricelist'].search([('advised_pricelist', '=', True)])
            if advised_price_pricelist:
                product_tmpl.advised_sale_price = advised_price_pricelist.with_context(uom=product_tmpl.uom_id.id).get_product_price(product_tmpl, 1.0, False)
                if len(product_tmpl.product_variant_ids.ids) == 1:
                    product_tmpl.product_variant_ids.get_advised_price()
            else:
                product_tmpl.advised_sale_price = 0


class SerelProductProduct(models.Model):
    _inherit = 'product.product'

    tag_product_ids = fields.Many2many('tag.product.template', 'product_product_tag_rel', 'product_id', 'tag_id', related="product_tmpl_id.tag_product_ids", string='Tags', readonly=True)
    pr_advised_sale_price = fields.Float(string='Pr Advised Sale Price', digits='Product Price', compute='get_advised_price', store=True)
    default_code = fields.Char(required=True)

    _sql_constraints = [
        ('unique_default_code', 'unique(default_code)', 'This reference already exists!')
    ]

    @api.model
    def create(self, vals):
        # self.ensure_one()
        product_tmpl_configurator = self.env['product.template'].search([('product_add_mode', '=', 'configurator'),
                                                                         ('id', '=', vals['product_tmpl_id'])])
        if vals['product_tmpl_id'] in product_tmpl_configurator.ids:
            ref = product_tmpl_configurator.default_code
            vals['default_code'] = ref + self.env['ir.sequence'].next_by_code('product.product')
            # res.default_code = ref + self.env['ir.sequence'].next_by_code('product.product')
            product_tmpl_configurator.default_code = ref
        # else:
            # res = super(SerelProductProduct, self).create(vals)
        return super(SerelProductProduct, self).create(vals)

    @api.depends('standard_price')
    def get_advised_price(self):
        """
        Set the advised price defined by the pricelist with the flag 'advised_pricelist' checked.
        """
        for product_product in self:
            advised_price_pricelist = self.env['product.pricelist'].search([('advised_pricelist', '=', True)])
            if advised_price_pricelist:
                product_product.pr_advised_sale_price = advised_price_pricelist.with_context(
                    uom=product_product.uom_id.id).get_product_price(product_product, 1.0, False)
            else:
                product_product.pr_advised_sale_price = 0


class SerelTagProduct(models.Model):
    _name = 'tag.product.template'
    _description = 'Tags for the products'

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Name')
    product_ids = fields.Many2many('product.template', 'product_template_tag_rel', 'tag_id', 'product_id', string='Products')
