from odoo import models, fields, api, _
from odoo.exceptions import UserError

class DJBCPosisiWipWizard(models.TransientModel):
    _name = "djbc.posisi.wip.wizard"
    _description = "DJBC Posisi WIP Report Wizard"
    
    date_start = fields.Date(string='Date Start', required=True)
    date_end = fields.Date(string='Date End', required=True)

    def call_djbc_posisi_wip(self):
        # ... (this method remains the same)
        cr = self.env.cr
        cr.execute("select djbc_posisi_wip(%s,%s)",(self.date_start, self.date_end))
        action = self.env['ir.actions.act_window']._for_xml_id("djbc_posisi_wip.posisi_wip_action")
        return action

    # --- Add this new method ---
    def generate_laporan_xls(self):
        self.ensure_one()
        # First, run the stored procedure to populate the table
        cr = self.env.cr
        cr.execute("select djbc_posisi_wip(%s,%s)", (self.date_start, self.date_end))
        
        # Then, prepare data for the report
        data = {
            'model': 'djbc.posisi.wip.wizard',
            'form': self.read()[0]
        }
        # Finally, call the report action
        return self.env.ref('djbc_posisi_wip.posisi_wip_xlsx').report_action(self, data=data)
    # -----------------------------

    @api.onchange('date_end')
    def onchange_date(self):
        # ... (this method remains the same)
        if self.date_start and self.date_end and self.date_start > self.date_end:
            return {
                'warning': {
                    'title': ('Warning'),
                    'message': ('Date End cannot be earlier than Date Start.')
                }
            }
            
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        # ... (this method remains the same)
        for rec in self:
            if rec.date_start > rec.date_end:
                raise UserError(_('Date End cannot be earlier than Date Start.'))