# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelResPartner(models.Model):
    _inherit = 'res.partner'

    def populate_categ_id(self, categ_id):
        """
        :param categ_id: The ID of the res partner category to apply on every res partner contains in self and their childs.
        """
        for partner in self:
            childs = self.search([('parent_id', '=', partner.id)])
            partner.with_context(populate_categ_id=True).write({'category_id': categ_id})
            if childs:
                childs.populate_categ_id()

    def write(self, values):
        """
        When a company has contacts, populate the tags of the company on its contacts.
        """
        for partner in self:
            if 'category_id' in values and not self.env.context.get('populate_categ_id', False):
                if partner.is_company:
                    childs = self.search([('parent_id', '=', partner.id)])
                    childs.populate_categ_id(values['category_id'])
        return super(SerelResPartner, self).write(values)
