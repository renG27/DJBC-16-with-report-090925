# -*- coding: utf-8 -*-
{
    'name': 'DJBC Laporan Posisi WIP',
    'version': '16.0.1.0.0',
    'summary': 'DJBC Laporan Posisi WIP',
    'description': 'DJBC Laporan Posisi WIP',
    'category': 'Extra Tools',
    'author': '',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc', 'report_xlsx'], # Add 'report_xlsx'
    'data': [
        'security/ir.model.access.csv',
        'reports/report.xml', # Add this line
        'views/posisi_wip.xml',
        'wizards/posisi_wip_wiz.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}