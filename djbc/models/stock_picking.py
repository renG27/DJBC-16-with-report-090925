# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcStockPicking(models.Model):
    _inherit = 'stock.picking'

    djbc_docs_id = fields.Many2one('djbc.docs', string='DJBC Document')