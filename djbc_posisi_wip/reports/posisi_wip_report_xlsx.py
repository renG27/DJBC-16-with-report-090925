# -*- coding: utf-8 -*-
from odoo import models

class PosisiWipXlsx(models.AbstractModel):
    _name = 'report.djbc_posisi_wip.posisi_wip_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Laporan Posisi WIP XLSX'

    def generate_xlsx_report(self, workbook, data, objects):
        # The wizard has already populated the 'djbc.posisi.wip' table.
        # We just need to search for all records in it.
        docs = self.env['djbc.posisi.wip'].search([])
        
        # Get data from the wizard form
        form_data = data.get('form', {})
        date_start = form_data.get('date_start')
        date_end = form_data.get('date_end')

        sheet = workbook.add_worksheet('Laporan Posisi WIP')

        # Cell formats
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        cell_format = workbook.add_format({'border': 1})
        date_format = workbook.add_format({'border': 1, 'num_format': 'dd/mm/yyyy'})

        # Report Header
        sheet.merge_range('A1:F2', 'Laporan Posisi WIP', title_format)
        sheet.write('A4', 'Periode:')
        sheet.write('B4', f'{date_start} s/d {date_end}')

        # Table Headers
        headers = [
            'Tgl Penerimaan', 'Kode Barang', 'Nama Barang',
            'Jumlah', 'Satuan', 'Warehouse'
        ]
        for col, header in enumerate(headers):
            sheet.write(6, col, header, header_format)

        # Table Data
        row = 7
        for doc in docs:
            sheet.write(row, 0, doc.tgl_penerimaan, date_format)
            sheet.write(row, 1, doc.kode_barang, cell_format)
            sheet.write(row, 2, doc.nama_barang, cell_format)
            sheet.write(row, 3, doc.jumlah, cell_format)
            sheet.write(row, 4, doc.satuan, cell_format)
            sheet.write(row, 5, doc.warehouse, cell_format)
            row += 1

        # Adjust column widths
        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 35)
        sheet.set_column('D:E', 12)
        sheet.set_column('F:F', 25)