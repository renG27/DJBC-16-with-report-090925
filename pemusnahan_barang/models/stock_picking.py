# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"
    

    @api.depends('picking_type_id')
    def _compute_picking_type_name_pemusnahan(self):
        for picking in self:
            picking.picking_type_name_pemusnahan = picking.picking_type_id.name if picking.picking_type_id else False

    picking_type_name_pemusnahan = fields.Char(
        string="Type Name",
        compute="_compute_picking_type_name_pemusnahan",
        store=True,
    )

    nomor_pemusnahan = fields.Char(
        string="Nomor Pemusnahan",
    )

    tanggal_pemusnahan = fields.Date(
        string="Tanggal Pemusnahan",
    )