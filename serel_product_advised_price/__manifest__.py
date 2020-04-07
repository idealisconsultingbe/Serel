# -*- coding: utf-8 -*-

{
    'name': "Serel Product Advised Price",
    'version': '1.0',
    'category': 'Product',
    'summary': 'Add fields in the Product model',
    'author': 'Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['base', 'product', 'sale', 'stock', 'mrp'],
    'price': 0,
    'currency': 'EUR',
    'data': [
        'data/serel_product_sequence.xml',
        'security/ir.model.access.csv',
        'views/serel_product_pricelist_view.xml',
        'views/serel_product_view.xml',
        'views/serel_tag_product_view.xml',
        'views/serel_sale_order_view.xml',
    ],

    'installable': True,
}