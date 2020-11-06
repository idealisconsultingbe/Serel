# -*- coding: utf-8 -*-

{
    'name': "Serel Product Advised Price",
    'version': '1.0',
    'category': 'Product',
    'summary': 'Add fields in the Product model',
    'author': 'Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'depends': ['base', 'product', 'sale'],
    'price': 0,
    'currency': 'EUR',
    'data': [
        'data/serel_product_sequence.xml',
        'data/serel_mail_notification_paynow_data.xml',
        'report/serel_report_saleorder_document_report.xml',
        'report/serel_delivery_document_report.xml',
        'report/serel_invoice_document_report.xml',
        'report/serel_stickers_1.xml',
        'report/serel_stickers_2.xml',
        'report/serel_stickers_3.xml',
        'security/ir.model.access.csv',
        'views/serel_product_pricelist_view.xml',
        'views/serel_product_view.xml',
        'views/serel_tag_product_view.xml',
        'views/serel_sale_order_view.xml',
        'views/serel_account_invoice_view.xml'
    ],

    'installable': True,
}