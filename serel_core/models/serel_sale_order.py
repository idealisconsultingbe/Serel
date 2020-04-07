# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SerelSaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_default_available_salesperson(self):
        """
        :return: Return all the users that are available for being set as salesperson.  An available person is a person that is a member of the sales team linked to the SO.
        """
        team_id = self._get_default_team() if not self.team_id else self.team_id
        sales_team = self.env['crm.team'].search([('id', '=', team_id.id)])
        salesperson = self.env['res.users']
        salesperson |= sales_team.user_id
        salesperson |= sales_team.member_ids
        return salesperson

    available_salesperson = fields.Many2many('res.users', string="Availables Sales Person", compute='_get_available_salesperson', default=_get_default_available_salesperson)

    @api.depends('team_id', 'team_id.user_id', 'team_id.member_ids')
    def _get_available_salesperson(self):
        """
        :return: Return all the users that are available for being set as salesperson.  An available person is a person that is a member of sales team linked to the SO.
        """
        for sale in self:
            salesperson = sale._get_default_available_salesperson()
            sale.write({'available_salesperson': [(6, 0, salesperson.ids)]})
