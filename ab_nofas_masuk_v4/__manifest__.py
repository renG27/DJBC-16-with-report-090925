# -*- coding: utf-8 -*-
{
    'name': 'DJBC Pemasukan V4',
    'version': '16.0.1.0.0',
    'summary': 'Laporan Pemasukan DJBC',
    'description': 'Laporan Pemasukan DJBC',
    'category': 'Extra Tools',
    'author': '',
    'website': '-',
    'license': 'LGPL-3',
    'depends': [
        'djbc',
        'purchase',
        'account',
        'report_xlsx'
    ],
    'data': [
        'security/ir.model.access.csv',
        # Add all UI files
        'wizards/nofas_masuk_wiz.xml',
        'views/nofas_masuk.xml',
        'views/menu.xml',
        'reports/report.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}