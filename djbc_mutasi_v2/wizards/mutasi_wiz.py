import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DJBCMutasiWizard(models.TransientModel):
    _name='djbc.mutasiwizardv2'

    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    djbc_category_id = fields.Many2one(comodel_name="djbc.categs", string="DJBC Category", required=False, )
    kategori = fields.Char(string="Kategori")
    
    def generate_laporan(self):
        self.ensure_one()
        cr=self.env.cr
        # _logger.info(self.djbc_category_id.id)
        cr.execute("select djbc_mutasi_v2(%s,%s,%s)",(self.date_start, self.date_end, self.djbc_category_id.id))
        
        # Return the action in the modern dictionary format
        return {
            'name': 'Laporan Mutasi',
            'type': 'ir.actions.act_window',
            'res_model': 'djbc.mutasi_v2',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def generate_laporan_xls(self):
        self.ensure_one()
        cr=self.env.cr
        cr.execute("select djbc_mutasi_v2(%s,%s,%s)",(self.date_start, self.date_end, self.djbc_category_id.id))
        data = {
            'model': 'djbc.mutasiwizardv2',
            'form': self.read()[0]
        }
        
        return self.env.ref('djbc_mutasi_v2.mutasi_xlsx').report_action(self, data=data)

    @api.onchange('date_start', 'date_end')
    def onchange_date(self):
        res={}
        if self.date_start and self.date_end and self.date_start > self.date_end:
            res = {'warning':{
                'title':('Warning'),
                'message':('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')}}
        if res:
            return res

    @api.onchange('djbc_category_id')
    def onchange_kategori(self):
        if self.djbc_category_id:
            self.kategori = self.djbc_category_id.name
        else:
            self.kategori = False
        return