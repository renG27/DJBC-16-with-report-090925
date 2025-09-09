from odoo import models

class PemusnahanXlsx(models.AbstractModel):
    _name = 'report.djbc_nofas_pemusnahan.pemusnahan_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Laporan Pemusnahan XLSX'

    def generate_xlsx_report(self, workbook, data, wizard_record):
        # Extract the date range from the data passed by the wizard.
        date_start = data['form'].get('date_start')
        date_end = data['form'].get('date_end')

        # Build the search domain to filter records by the selected dates.
        domain = [
            ('tgl_pemusnahan', '>=', date_start),
            ('tgl_pemusnahan', '<=', date_end),
        ]

        # Search the SQL View model with the correct domain.
        # This is the fix: instead of search([]), we use our domain.
        lines = self.env['djbc.nofas_musnah'].search(domain, order='tgl_pemusnahan asc')

        # --- The rest of the report generation logic remains the same ---

        sheet = workbook.add_worksheet('Pemusnahan')
        format1 = workbook.add_format({'font_name': 'Arial', 'font_size': 13, 'align': 'center', 'bold': True})
        format2 = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center'})
        format_header = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center', 'bold': False})
        
        # The report title now correctly reflects the filtered period.
        sheet.merge_range('A1:G1', 'Laporan Pemusnahan Barang', format1)
        sheet.merge_range('A2:G2', f"Periode: {date_start} s.d {date_end}", format1)

        sheet.write(3, 0, 'No', format_header)
        sheet.write(3, 1, 'Nomor Pemusnahan', format_header)
        sheet.write(3, 2, 'Tanggal Pemusnahan', format_header)
        sheet.write(3, 3, 'Kode Barang', format_header)
        sheet.write(3, 4, 'Nama Barang', format_header)
        sheet.write(3, 5, 'Jumlah', format_header)
        sheet.write(3, 6, 'Satuan', format_header)
        
        row_num = 3
        no = 0
        for obj in lines:
            row_num += 1
            no += 1
            sheet.write(row_num, 0, no, format2)
            sheet.write(row_num, 1, obj.no_pemusnahan, format2)
            # Dates must be converted to string for xlsxwriter
            sheet.write(row_num, 2, str(obj.tgl_pemusnahan), format2)
            sheet.write(row_num, 3, obj.kode_barang, format2)
            sheet.write(row_num, 4, obj.nama_barang, format2)
            sheet.write(row_num, 5, obj.jumlah, format2)
            sheet.write(row_num, 6, obj.satuan, format2)