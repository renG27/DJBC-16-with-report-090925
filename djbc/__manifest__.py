# -*- coding: utf-8 -*-
{
    'name': "DJBC Apps",
    'summary': "Laporan IT Inventory DJBC",
    'description': """
        Laporan IT Inventory DJBC untuk fasilitas TPB (KB, PLB, GB), KITE dan Non Fasilitas (Umum).
    """,
    'author': "Oktovan Rezman",
    'website': "-",
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'version': '16.0.1.0.0',

    'depends': [
        'stock',
        'product',
        'account',
        'report_xlsx',
        'base_import',
        'web',
        # 'stock_barcode' is not needed
    ],
    'assets': {
    'web.assets_backend': [
        'djbc/static/src/js/import_button.js',
    ],
    },
    
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/categs.xml',
        'views/container.xml',
        'views/doctype.xml',
        'views/docs.xml',
        'views/hscode.xml',
        # Add the final view files below
        'views/product_template.xml',
        'views/stock_location.xml',
        'views/stock_move_line.xml',
        'views/stock_picking.xml',
        'views/menu.xml',
    ],
    'application': True,
}