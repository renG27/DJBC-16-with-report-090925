import logging
from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)

class DJBCNofasPemusnahan(models.Model):
    _auto = False
    _name = 'djbc.nofas_musnah'
    _description = 'DJBC Laporan Pemusnahan (View)'
    _rec_name = 'no_pemusnahan'

    no_pemusnahan = fields.Char(string='Nomor Pemusnahan', readonly=True)
    tgl_pemusnahan = fields.Date(string='Tanggal Pemusnahan', readonly=True)
    kode_barang = fields.Char(string='Kode Barang', readonly=True)
    nama_barang = fields.Char(string='Nama Barang', readonly=True)
    jumlah = fields.Float(string='Jumlah', readonly=True)
    satuan = fields.Char(string='Satuan', readonly=True)
    location = fields.Char(string='Location', readonly=True)
    warehouse = fields.Char(string='Warehouse', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)

        # Final version using an f-string for safe and modern formatting
        query = f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    xx.id AS id,
                    y.nomor_pemusnahan as no_pemusnahan,
                    y.tanggal_pemusnahan as tgl_pemusnahan,
                    xz.default_code as kode_barang,
                    xz.name as nama_barang,
                    xx.product_uom_qty as jumlah,
                    yx.name as satuan,
                    t5.name as location,
                    t8.name as warehouse
                FROM
                    stock_move xx
                    JOIN stock_picking y ON xx.picking_id = y.id
                    JOIN stock_picking_type t6 ON t6.id = y.picking_type_id
                    LEFT JOIN res_partner z ON z.id=y.partner_id
                    LEFT JOIN res_partner t7 ON t7.id = y.owner_id
                    JOIN stock_location t5 ON t5.id = xx.location_id
                    JOIN stock_location t8 ON t8.id = t5.location_id
                    JOIN product_product xy ON xy.id=xx.product_id
                    JOIN product_template xz ON xz.id=xy.product_tmpl_id
                    JOIN uom_uom yx ON yx.id=xx.product_uom
                WHERE
                    xx.state = 'done'
                    AND (t6.name ->> 'en_US') LIKE 'Pemusnahan%'
                ORDER BY
                    y.tanggal_pemusnahan
            )
        """
        self.env.cr.execute(query)