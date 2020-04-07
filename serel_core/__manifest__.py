# -*- coding: utf-8 -*-

{
    'name': "Serel Core",
    'version': '1.0',
    'category': 'All',
    'summary': 'Add Logic in the different models of Odoo in order to correspond with the way of working of the Serel company.',
    'author': 'Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['base', 'sale'],
    'price': 0,
    'currency': 'EUR',
    'data': [
        'views/serel_res_partner_view.xml',
        'views/serel_sale_order_view.xml',
    ],

    'installable': True,
}