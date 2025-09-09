# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DJBCNofasMasukWiz(models.TransientModel):
    _name = "djbc.nofas.masuk.wizard.v4"
    _description = "DJBC Laporan Pemasukan Wizard V4"

    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)

    def generate_laporan(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id("ab_nofas_masuk_v4.nofas_masuk_action")
        # Add a domain to the action based on the wizard's dates
        action['domain'] = [
            ('tgl_penerimaan', '>=', self.date_start),
            ('tgl_penerimaan', '<=', self.date_end)
        ]
        return action

    @api.onchange('date_end')
    def onchange_date(self):
        if self.date_start and self.date_end and self.date_start > self.date_end:
            return {'warning': {
                'title': ('Warning'),
                'message': ('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')
            }}

    def generate_laporan_xls(self):
        self.ensure_one()
        data = {
            'model': self._name,
            'form': self.read()[0]
        }
        return self.env.ref('ab_nofas_masuk_v4.nofas_masuk_xlsx').report_action(self, data=data)