import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCPosisiWIP(models.Model):
    _name = 'djbc.posisi.wip'
    _description = 'DJBC Laporan Posisi WIP'

    tgl_penerimaan = fields.Date(string='Tgl Penerimaan')
    kode_barang = fields.Char(string='Kode Barang')
    nama_barang = fields.Char(string='Nama Barang')
    jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    warehouse = fields.Char(string='Warehouse')

    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_posisi_wip(DATE, DATE);
       CREATE OR REPLACE FUNCTION djbc_posisi_wip(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$

DECLARE
	
	csr cursor for
    	SELECT date(min(sq.in_date)) as tgl_penerimaan,p.default_code as kode_barang,pt.name as nama_barang,
	round(cast(sum(sq.quantity) as "numeric"),2) as jumlah,u.name as satuan,sl.complete_name as warehouse
	FROM stock_quant sq
	LEFT JOIN stock_location sl ON sq.location_id=sl.id
	LEFT JOIN product_product p ON sq.product_id=p.id
	LEFT JOIN product_template pt ON p.product_tmpl_id=pt.id
	LEFT JOIN uom_uom u ON pt.uom_id=u.id
	WHERE sl.name LIKE 'PROD%' 
	GROUP BY sq.product_id,sq.in_date,p.default_code,pt.name,u.name,sl.complete_name
	having sum(sq.quantity) > 0 ;
	
	
			
begin

	delete from djbc_posisi_wip;
	
	
	  for rec in csr loop
		insert into djbc_posisi_wip (tgl_penerimaan, kode_barang,
			nama_barang, jumlah, satuan, warehouse) 
			values (rec.tgl_penerimaan, rec.kode_barang, rec.nama_barang, rec.jumlah, rec.satuan, rec.warehouse) ;
	  end loop;


end;

$BODY$
LANGUAGE plpgsql;
        """)