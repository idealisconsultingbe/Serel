# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SerelProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    advised_pricelist = fields.Boolean(string='Is The Advised Pricelist', default=False)

    def write(self, values):
        """
        Make sure that only one pricelist have the flag 'advised_pricelist' set to True.
        """
        if values.get('advised_pricelist', False):
            if len(self.ids) > 1:
                raise UserError(_("You cannot have more than one pricelist with the flag 'Advised Pricelist' set to True"))
            else:
                advised_pricelist = self.search([('advised_pricelist', '=', True)])
                advised_pricelist.write({'advised_pricelist': False})
        return super(SerelProductPricelist, self).write(values)
