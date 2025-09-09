# -*- coding: utf-8 -*-
from odoo import models

class MutasiXlsx(models.AbstractModel):
    # The name must match the "name" attribute in your report's <report> tag
    _name = 'report.djbc_mutasi_v2.mutasi_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Laporan Mutasi XLSX'

    def generate_xlsx_report(self, workbook, data, objects):
        # Get the records that the report will be based on.
        # The wizard populates the 'djbc.mutasi_v2' table, so we search for all records in it.
        docs = self.env['djbc.mutasi_v2'].search([])
        
        # Get the form data passed from the wizard
        form_data = data.get('form', {})
        date_start = form_data.get('date_start')
        date_end = form_data.get('date_end')
        kategori = form_data.get('kategori', 'Semua Kategori')

        # Add a worksheet
        sheet = workbook.add_worksheet('Laporan Mutasi')

        # Define cell formats
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        cell_format = workbook.add_format({'border': 1})
        
        # --- Report Header ---
        sheet.merge_range('A1:K2', 'Laporan Mutasi', title_format)
        sheet.write('A4', 'Periode:')
        sheet.write('B4', f'{date_start} s/d {date_end}')
        sheet.write('A5', 'Kategori:')
        sheet.write('B5', kategori)
        
        # --- Table Headers ---
        headers = [
            'Kode Barang', 'Nama Barang', 'Satuan', 'Saldo Awal', 'Pemasukan',
            'Pengeluaran', 'Penyesuaian', 'Stock Opname', 'Saldo Akhir', 'Selisih', 'Keterangan'
        ]
        for col, header in enumerate(headers):
            sheet.write(6, col, header, header_format)

        # --- Table Data ---
        row = 7
        for doc in docs:
            sheet.write(row, 0, doc.kode_barang, cell_format)
            sheet.write(row, 1, doc.nama_barang, cell_format)
            sheet.write(row, 2, doc.satuan, cell_format)
            sheet.write(row, 3, doc.saldo_awal, cell_format)
            sheet.write(row, 4, doc.pemasukan, cell_format)
            sheet.write(row, 5, doc.pengeluaran, cell_format)
            sheet.write(row, 6, doc.penyesuaian, cell_format)
            sheet.write(row, 7, doc.stock_opname, cell_format)
            sheet.write(row, 8, doc.saldo_akhir, cell_format)
            sheet.write(row, 9, doc.selisih, cell_format)
            sheet.write(row, 10, doc.keterangan, cell_format)
            row += 1
            
        # Adjust column widths
        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:K', 12)