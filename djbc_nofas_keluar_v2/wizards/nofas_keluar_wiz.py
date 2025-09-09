from odoo import models, fields, api

class DJBCNofasKeluarV2Wizard(models.TransientModel):
    _name = "djbc.nofas.keluar.v2.wizard"
    _description = "Wizard Laporan Pengeluaran"

    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)

    def call_djbc_nofas_keluar_v2(self):
        # ... (this method remains the same)
        self.ensure_one()
        domain = [
            ('tgl_dok', '>=', self.date_start),
            ('tgl_dok', '<=', self.date_end)
        ]
        return {
            'name': 'Laporan Pengeluaran',
            'type': 'ir.actions.act_window',
            'res_model': 'djbc.nofas_keluar_v2',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

    # --- Add this new method ---
    def generate_laporan_xls(self):
        self.ensure_one()
        data = {
            'model': 'djbc.nofas.keluar.v2.wizard',
            'form': self.read()[0]
        }
        return self.env.ref('djbc_nofas_keluar_v2.nofas_keluar_xlsx').report_action(self, data=data)
    # -----------------------------

    @api.onchange('date_start', 'date_end')
    def onchange_date(self):
        # ... (this method remains the same)
        res = {}
        if self.date_start and self.date_end and self.date_start > self.date_end:
            res = {'warning': {
                'title': ('Warning'),
                'message': ('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')}}
        return res