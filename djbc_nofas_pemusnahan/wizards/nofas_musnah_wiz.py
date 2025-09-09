from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DJBCNofasMusnahWizard(models.TransientModel):
    _name = "djbc.nofas.musnah.wizard"
    _description = "DJBC Nofas Musnah Wizard"

    # Fields are now marked as required=True for better data validation.
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)

    # The @api.multi decorator has been removed.
    # The method now returns a dictionary, which is a standard Odoo action.
    def call_djbc_nofas_musnah(self):
        self.ensure_one() # Ensures the method runs on a single wizard record.

        # This dictionary is an 'ir.actions.act_window'.
        # It tells the client what view to open.
        return {
            'name': _('Laporan Pemusnahan'),
            'type': 'ir.actions.act_window',
            'res_model': 'djbc.nofas_musnah', # Our SQL View model
            'view_mode': 'tree,form',
            # This is the critical part: we build a domain to filter the records
            # based on the dates selected in the wizard.
            'domain': [
                ('tgl_pemusnahan', '>=', self.date_start),
                ('tgl_pemusnahan', '<=', self.date_end)
            ],
        }

    # The @api.multi decorator has been removed.
    def generate_laporan_pemusnahan_xls(self):
        self.ensure_one()
        # The direct SQL call cr.execute(...) is removed. It's no longer needed.
        data = {
            'model': 'djbc.nofas.musnah.wizard',
            'form': self.read()[0]
        }
        # This line correctly calls the report action. It remains the same.
        return self.env.ref('djbc_nofas_pemusnahan.pemusnahan_xlsx').report_action(self, data=data)
        
    # The old onchange method has been replaced with a constraint.
    # A constraint is a more robust way to validate data.
    # It runs when the record is saved and prevents invalid data.
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        if self.date_start > self.date_end:
            raise UserError(_('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai'))