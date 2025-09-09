# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)

class DJBCNofasMasuk(models.Model):
    _name = 'djbc.nofas_masuk_v4'
    _description = 'DJBC Laporan Pemasukan'
    _rec_name = 'no_dok'
    _auto = False

    jenis_dok = fields.Char(string='Jenis Dokumen', readonly=True)
    no_dok = fields.Char(string='Nomor Pendaftaran', readonly=True)
    tgl_dok = fields.Date(string='Tgl Pendaftaran', readonly=True)
    no_penerimaan = fields.Char(string='Nomor Penerimaan', readonly=True)
    tgl_penerimaan = fields.Datetime(string='Tgl Penerimaan', readonly=True)
    pengirim = fields.Char(string='Pengirim Barang', readonly=True)
    kode_barang = fields.Char(string='Kode Barang', readonly=True)
    nama_barang = fields.Char(string='Nama Barang', readonly=True)
    jumlah = fields.Float(string='Jumlah', readonly=True)
    satuan = fields.Char(string='Satuan', readonly=True)
    nilai = fields.Float(string='Nilai', readonly=True)
    currency = fields.Char(string='Currency', readonly=True)
    warehouse = fields.Char(string='Warehouse', readonly=True)

    @api.model
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW %s AS (
            SELECT
                sml.id,
                doc.code as jenis_dok,
                bc.no_dok,
                bc.tgl_dok,
                sp.name as no_penerimaan,
                sp.date_done AS tgl_penerimaan,
                rp.name AS pengirim,
                pt.default_code as kode_barang,
                pt.name as nama_barang,
                sml.qty_done as jumlah,
                uom.name AS satuan,
                (sml.qty_done * sm.price_unit) AS nilai,
                cur.name AS currency,
                wh.code AS warehouse
            FROM
                stock_move_line sml
                JOIN stock_move sm ON sml.move_id = sm.id
                JOIN stock_picking sp ON sml.picking_id = sp.id
                -- Correct Odoo 16 Join: Link picking to PO via the 'origin' field
                LEFT JOIN purchase_order po ON sp.origin = po.name
                LEFT JOIN res_currency cur ON po.currency_id = cur.id
                -- Other standard joins
                JOIN stock_picking_type spt ON sp.picking_type_id = spt.id
                JOIN product_product p ON sml.product_id = p.id
                JOIN product_template pt ON p.product_tmpl_id = pt.id
                JOIN uom_uom uom ON sml.product_uom_id = uom.id
                LEFT JOIN res_partner rp ON sp.partner_id = rp.id
                LEFT JOIN djbc_docs bc ON sp.djbc_docs_id = bc.id
                LEFT JOIN djbc_doctype doc ON bc.jenis_dok = doc.id
                LEFT JOIN stock_warehouse wh ON sp.picking_type_id = wh.in_type_id
            WHERE
                spt.code = 'incoming'
                AND sp.djbc_docs_id IS NOT NULL
                AND sp.state = 'done'
        )""" % (self._table,))