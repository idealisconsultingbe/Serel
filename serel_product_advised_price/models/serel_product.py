# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class SerelProductTmpl(models.Model):
    _inherit = 'product.template'

    tag_product_ids = fields.Many2many('tag.product.template', 'product_template_tag_rel', 'product_id', 'tag_id',
                                       string='Tags')
    advised_sale_price = fields.Float(string='Advised Sale Price', digits='Product Price', compute='get_advised_price',
                                      store=True)
    sequence = fields.Integer(string='Sequence', default=0)
    product_tmpl_sequence = fields.Integer(string='Digits for Variant Sequence', default=0,
                                           help='Number of Digits for the generated Product Variant Reference')
    default_code = fields.Char('Internal Reference', compute=False, inverse=False, store=True)
    sticker_label = fields.Char(string='Sticker Label', store=True, readonly=False, size=10)

    _sql_constraints = [
        ('unique_default_code', 'unique(default_code)', 'This reference already exists!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        templates = super(SerelProductTmpl, self).create(vals_list)
        if "create_product_product" not in self._context:
            templates._create_variant_ids()

        # This is needed to set given values to first variant after creation
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if vals.get('barcode'):
                related_vals['barcode'] = vals['barcode']
            # if vals.get('default_code'):
            #     related_vals['default_code'] = vals['default_code']
            if vals.get('standard_price'):
                related_vals['standard_price'] = vals['standard_price']
            if vals.get('volume'):
                related_vals['volume'] = vals['volume']
            if vals.get('weight'):
                related_vals['weight'] = vals['weight']
            # Please do forward port
            if vals.get('packaging_ids'):
                related_vals['packaging_ids'] = vals['packaging_ids']
            if vals.get('name'):
                related_vals['sticker_label'] = vals['name']
            if related_vals:
                template.write(related_vals)

        return templates

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if 'default_code' not in default:
            default['default_code'] = self.default_code + self.env['ir.sequence'].next_by_code('product.product')
        return super(SerelProductTmpl, self).copy(default=default)
    
    @api.depends('standard_price')
    def get_advised_price(self):
        """
        Set the advised price defined by the pricelist with the flag 'advised_pricelist' checked.
        """
        for product_tmpl in self:
            advised_price_pricelist = self.env['product.pricelist'].search([('advised_pricelist', '=', True)])
            # product_tmpl_ids in the if-condition to avoid an error while creating a product
            if advised_price_pricelist and product_tmpl.ids:
                product_tmpl.advised_sale_price = advised_price_pricelist.with_context(uom=product_tmpl.uom_id.id).get_product_price(product_tmpl, 1.0, False)
                if len(product_tmpl.product_variant_ids.ids) == 1:
                    product_tmpl.product_variant_ids.get_advised_price()
            else:
                product_tmpl.advised_sale_price = 0

    def _create_product_variant(self, combination, log_warning=False):
        """ Create if necessary and possible and return the product variant
        matching the given combination for this template.

        It is possible to create only if the template has dynamic attributes
        and the combination itself is possible.
        If we are in this case and the variant already exists but it is
        archived, it is activated instead of being created again.

        :param combination: the combination for which to get or create variant.
            The combination must contain all necessary attributes, including
            those of type no_variant. Indeed even though those attributes won't
            be included in the variant if newly created, they are needed when
            checking if the combination is possible.
        :type combination: recordset of `product.template.attribute.value`

        :param log_warning: whether a warning should be logged on fail
        :type log_warning: bool

        :return: the product variant matching the combination or none
        :rtype: recordset of `product.product`
        """
        self.ensure_one()

        Product = self.env['product.product']

        product_variant = self._get_variant_for_combination(combination)
        if product_variant:
            if not product_variant.active and self.has_dynamic_attributes() and self._is_combination_possible(combination):
                product_variant.active = True
            return product_variant

        if not self.has_dynamic_attributes():
            if log_warning:
                _logger.warning('The user #%s tried to create a variant for the non-dynamic product %s.' % (self.env.user.id, self.id))
            return Product

        if not self._is_combination_possible(combination):
            if log_warning:
                _logger.warning('The user #%s tried to create an invalid variant for the product %s.' % (self.env.user.id, self.id))
            return Product

        self.sequence += 1
        return Product.sudo().create({
            'product_tmpl_id': self.id,
            'product_template_attribute_value_ids': [(6, 0, combination._without_no_variant_attributes().ids),],
            'default_code': self.default_code + (str(self.sequence)).zfill(self.product_tmpl_sequence),
        })


class SerelProductProduct(models.Model):
    _inherit = 'product.product'

    tag_product_ids = fields.Many2many('tag.product.template', 'product_product_tag_rel', 'product_id', 'tag_id',
                                       related="product_tmpl_id.tag_product_ids", string='Tags', readonly=True)
    pr_advised_sale_price = fields.Float(string='Pr Advised Sale Price', digits='Product Price',
                                         compute='get_advised_price', store=True)
    sticker_label = fields.Char(string='Sticker Label', compute='_compute_sticker_label', store=True, readonly=False)

    _sql_constraints = [
        ('unique_default_code', 'unique(default_code)', 'This reference already exists!')
    ]

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

    @api.depends('name')
    def _compute_sticker_label(self):
        for product in self:
            product.sticker_label = product.name

    def get_product_multiline_description_sale(self):
        """ Compute a multiline description of this product, in the context of sales
                (do not use for purchases or other display reasons that don't intend to use "description_sale").
            It will often be used as the default description of a sale order line referencing this product.
        """
        name = self.display_name
        if self.description_sale:
            name = self.description_sale

        return name

    def get_url_img(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('report.url') or self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = base_url + '/serel_core/static/src/img/sigleblack.jpg'
        return url


class SerelTagProduct(models.Model):
    _name = 'tag.product.template'
    _description = 'Tags for the products'

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Name')
    product_ids = fields.Many2many('product.template', 'product_template_tag_rel', 'tag_id', 'product_id', string='Products')
