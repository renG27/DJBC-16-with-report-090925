# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    sisa_qty = fields.Float(string='Sisa Qty')
    jumlah_kemasan = fields.Float(string="Jumlah Kemasan")
    satuan_kemasan = fields.Char(string="Satuan Kemasan")
    djbc_masuk_flag = fields.Boolean(related='move_id.djbc_masuk_flag', string='DJBC Masuk', store=True)
    djbc_keluar = fields.Boolean(related='move_id.djbc_keluar', string='DJBC Keluar', store=True)