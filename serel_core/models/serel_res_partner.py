# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_default_available_salesperson(self):
        """
        :return: Return all the users that are available for being set as salesperson.  An available person is a person that is a member of a sales team.
        """
        sales_team = self.env['crm.team'].search([])
        salesperson = self.env['res.users']
        for team in sales_team:
            salesperson |= team.user_id
            salesperson |= team.member_ids
        return salesperson

    available_salesperson = fields.Many2many('res.users', string="Availables Sales Person", compute='_get_available_salesperson', default=_get_default_available_salesperson)

    def _get_available_salesperson(self):
        """
        :return: Return all the users that are available for being set as salesperson.
        """
        salesperson = self._get_default_available_salesperson()
        self.write({'available_salesperson': [(6, 0, salesperson.ids)]})
