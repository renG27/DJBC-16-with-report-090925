import logging
from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)

class DJBCNofasKeluarV2(models.Model):
    _name = 'djbc.nofas_keluar_v2'
    _description = 'DJBC Laporan Pengeluaran (View)'
    _auto = False
    _rec_name = 'no_dok'

    # Existing Fields
    jenis_dok = fields.Char(string='Jenis Dokumen', readonly=True)
    tgl_dok = fields.Date(string='Tgl Pendaftaran', readonly=True)
    no_dok = fields.Char(string='Nomor Pendaftaran', readonly=True)
    no_pengeluaran = fields.Many2one("stock.picking", string="Nomor Pengeluaran", readonly=True)
    tgl_pengeluaran = fields.Datetime(string='Tgl Pengeluaran', readonly=True)
    penerima = fields.Char(string='Penerima Barang', readonly=True)
    pemilik = fields.Char(string='Pemilik Barang', readonly=True)
    hs_code = fields.Char(string='HS Code', readonly=True)
    kode_barang = fields.Char(string='Kode Barang', readonly=True)
    nama_barang = fields.Char(string='Nama Barang', readonly=True)
    jumlah = fields.Float(string='Jumlah', readonly=True)
    satuan = fields.Char(string='Satuan', readonly=True)
    jumlah_kemasan = fields.Float(string='Jumlah Kemasan', readonly=True)
    satuan_kemasan = fields.Char(string='Satuan Kemasan', readonly=True)
    nilai = fields.Float(string='Nilai', readonly=True)
    currency = fields.Char(string='Currency', readonly=True)
    location = fields.Char(string='Location', readonly=True)
    warehouse = fields.Char(string='Warehouse', readonly=True)
    alm_wh = fields.Char(string='Alamat Warehouse', readonly=True)
    kota_wh = fields.Char(string='Kota', readonly=True)
    
    # --- Missing Fields to Add ---
    no_aju = fields.Char(string='Nomor Aju', readonly=True)
    tgl_aju = fields.Date(string='Tgl Aju', readonly=True)
    no_bl = fields.Char(string='Nomor B/L', readonly=True)
    tgl_bl = fields.Date(string='Tgl B/L', readonly=True)
    no_cont = fields.Char(string='Nomor Container', readonly=True)
    # -----------------------------

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    xx.id as id,
                    t3.code as jenis_dok,
                    x.no_dok as no_dok,
                    x.tgl_dok,
                    y.id as no_pengeluaran,
                    y.date_done as tgl_pengeluaran,
                    z.name as penerima,
                    xy.default_code as kode_barang,
                    pt.name as nama_barang,
                    xx.product_uom_qty as jumlah,
                    uom.name as satuan,
                    (case
                        when b1.price_subtotal is not null then d1.name
                        when yz.price_subtotal is not null then zx.name
                        else null
                    end) as currency,
                    (case
                        when b1.price_subtotal is not null then b1.price_subtotal
                        when yz.price_subtotal is not null then yz.price_subtotal
                        else 0.0
                    end) as nilai,
                    x.no_bl,
                    x.tgl_bl,
                    x.no_aju,
                    x.tgl_aju,
                    x.no_cont,
                    sml.jumlah_kemasan as jumlah_kemasan,
                    sml.satuan_kemasan as satuan_kemasan,
                    t4.code as hs_code,
                    t5.name as location,
                    t7.name as pemilik,
                    wh.name as warehouse,
                    wh_partner.street as alm_wh,
                    wh_partner.city as kota_wh
                FROM
                    stock_move xx
                    LEFT JOIN stock_move_line sml ON sml.move_id = xx.id
                    JOIN stock_picking y ON xx.picking_id = y.id
                    JOIN stock_picking_type t6 ON t6.id = y.picking_type_id
                    JOIN djbc_docs x ON x.id = y.djbc_docs_id
                    JOIN djbc_doctype t3 ON t3.id = x.jenis_dok
                    JOIN res_partner z ON z.id = y.partner_id
                    LEFT JOIN res_partner t7 ON t7.id = y.owner_id
                    JOIN stock_location t5 ON t5.id = xx.location_dest_id
                    LEFT JOIN stock_warehouse wh ON wh.id = t6.warehouse_id
                    LEFT JOIN res_partner wh_partner ON wh_partner.id = wh.partner_id
                    JOIN product_product xy ON xy.id = xx.product_id
                    JOIN product_template pt ON pt.id = xy.product_tmpl_id
                    LEFT JOIN djbc_hscode t4 ON t4.id = pt.hscode
                    JOIN uom_uom uom ON uom.id = xx.product_uom
                    LEFT JOIN sale_order_line yz ON yz.id = xx.sale_line_id
                    LEFT JOIN res_currency zx ON zx.id = yz.currency_id
                    LEFT JOIN stock_move_invoice_line_rel a1 ON xx.id = a1.move_id
                    LEFT JOIN account_move_line b1 ON a1.invoice_line_id = b1.id
                    LEFT JOIN account_move c1 ON b1.move_id = c1.id
                    LEFT JOIN res_currency d1 ON d1.id = c1.currency_id
                WHERE
                    xx.state = 'done'
                    AND t6.code = 'outgoing'
                GROUP BY
                    xx.id, t3.code, x.no_dok, x.tgl_dok, y.id, y.date_done, z.name, xy.default_code, pt.name, uom.name,
                    d1.name, yz.currency_id, zx.name, b1.price_subtotal, yz.price_subtotal, x.no_bl, x.tgl_bl, x.no_aju, x.tgl_aju, x.no_cont,
                    sml.jumlah_kemasan, sml.satuan_kemasan, t4.code, t5.name, t7.name, wh.name, wh_partner.street, wh_partner.city
            )
        """ % (self._table,))