from odoo import models, fields, api

class DJBCMutasi(models.Model):
    _name='djbc.mutasi_v2'
    _description='DJBC Laporan Mutasi'

    tgl_mulai = fields.Date(string = 'Tanggal Mulai')
    tgl_akhir = fields.Date(string = 'Tanggal Akhir')
    product_id = fields.Many2one('product.product', string='Product', visible=False)
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    saldo_awal=fields.Float(string='Saldo Awal')
    pemasukan=fields.Float(string='Pemasukan')
    pengeluaran=fields.Float(string='Pengeluaran')
    penyesuaian=fields.Float(string='Penyesuaian')
    stock_opname=fields.Float(string='Stock Opname')
    saldo_akhir=fields.Float(string='Saldo Akhir')
    selisih=fields.Float(string='Selisih')
    keterangan=fields.Char(string='Keterangan')
    location=fields.Char(string='Location')
    satuan=fields.Char(string="Satuan")
    warehouse=fields.Char(string='Warehouse')
    stock_move_lines = fields.One2many(
        'stock.move.line',
        string="Filtered Stock Move Lines",
        compute='_compute_stock_move_lines',
        domain="[('product_id.default_code', '=', kode_barang)]",
    )

    @api.depends('kode_barang', 'tgl_mulai', 'tgl_akhir')
    def _compute_stock_move_lines(self):
        for record in self:
            if record.kode_barang and record.tgl_mulai and record.tgl_akhir:
                record.stock_move_lines = self.env['stock.move.line'].search([
                    ('product_id.default_code', '=', record.kode_barang),
                    ('date', '>=', record.tgl_mulai),
                    ('date', '<=', record.tgl_akhir),
                ])
            else:
                record.stock_move_lines = False
    
    @api.model
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_mutasi_v2(DATE, DATE, INTEGER);
        CREATE OR REPLACE FUNCTION djbc_mutasi_v2(date_start DATE, date_end DATE, v_djbc_category_id INTEGER)
RETURNS VOID AS $BODY$

DECLARE
	v_date_start DATE;
	v_date_end DATE;


BEGIN
	v_date_start = date_start;
	v_date_end = date_end;
	delete from djbc_mutasi_v2;

    -- IF ( v_djbc_category_id IN (2,17,18,21,23)) THEN

	-- ELSE
		--insert into djbc_mutasi_v2 (kode_barang, nama_barang, saldo_awal, pemasukan, pengeluaran, penyesuaian, stock_opname, saldo_akhir, selisih,satuan, keterangan, location, warehouse, tgl_mulai, tgl_akhir)
			insert into djbc_mutasi_v2 (kode_barang, nama_barang, saldo_awal, pemasukan, pengeluaran, penyesuaian, stock_opname, saldo_akhir, selisih,satuan, keterangan, location, warehouse,tgl_mulai, tgl_akhir)
			select hdr.default_code,hdr.nama,
			case when sal.saldo is null then 0 else sal.saldo end as saldo,
			case when masuk.masuk is null then 0 else masuk.masuk end as masuk, 
			case when keluar.keluar is null then 0 else keluar.keluar end as keluar, 0.00,0.00,
			case when sal.saldo is null and masuk.masuk is null and keluar.keluar is null then 0  
				when sal.saldo is null and masuk.masuk is null then (0 - keluar.keluar)
				when sal.saldo is null and keluar.keluar is null then masuk.masuk 
				when masuk.masuk is null and keluar.keluar is null then sal.saldo  
				when sal.saldo is null then masuk.masuk-keluar.keluar 
				when masuk.masuk is null then sal.saldo-keluar.keluar 
				when keluar.keluar is null then sal.saldo+masuk.masuk else
				sal.saldo+masuk.masuk-keluar.keluar end as saldo_akhir,
				0.00,hdr.satuan,' sesuai','WH/Stock','WH',v_date_start,v_date_end
			from 
			-- Header
			(select pp.id,pp.default_code,tmp.name as nama,d.name as kategori,uom.name as satuan
			from ( select id,product_tmpl_id,default_code from product_product GROUP BY id ) pp
			left join product_template tmp on pp.product_tmpl_id=tmp.id
			left join djbc_categs d on tmp.djbc_category_id=d.id
			left join uom_uom uom on tmp.uom_id=uom.id
			where tmp.djbc_category_id = v_djbc_category_id
			) hdr
			left join 
			-- Saldo awal tinggal ganti date
			(select a.product_id as product_id,sum(a.masuk) as saldo from
			(select sm.product_id,sum(sm.product_uom_qty) as masuk,uom.name from stock_move sm
			left join uom_uom uom on sm.product_uom=uom.id
			left join stock_location sli on sm.location_id=sli.id
			where date(sm.date) < v_date_start and state = 'done' and 
			(sli.location_id=2 or sli.location_id=3)
			group by sm.product_id,uom.name
			union all
			select sm.product_id,sum(sm.product_uom_qty)*-1 as masuk,uom.name from stock_move sm
			left join uom_uom uom on sm.product_uom=uom.id
			left join stock_location slo on sm.location_dest_id=slo.id
			where date(sm.date) < v_date_start and state = 'done' and 
			(slo.location_id=2 or slo.location_id=3) 
			group by sm.product_id,uom.name) a
			group by a.product_id ) sal on hdr.id=sal.product_id
			left join 
			-- Pemasukan
			(select sm.product_id,sum(sm.product_uom_qty) as masuk from stock_move sm
			left join stock_location sli on sm.location_id=sli.id
			where (date(sm.date) >= v_date_start and date(sm.date) <= v_date_end) and state = 'done' and 
			(sli.location_id=2 or sli.location_id=3)
			group by sm.product_id) masuk on hdr.id=masuk.product_id
			left join
			-- Pengeluaran
			(select sm.product_id,sum(sm.product_uom_qty) as keluar from stock_move sm
			left join stock_location slo on sm.location_dest_id=slo.id
			left join stock_picking sp on sm.picking_id = sp.id
			where (date(sm.date) >= v_date_start and date(sm.date) <= v_date_end) and sm.state = 'done' and 
			((slo.location_id=2 or slo.location_id=3) or sp.picking_type_id = 9)
			group by sm.product_id) keluar on hdr.id=keluar.product_id
			--where tmp.djbc_category_id = v_djbc_category_id
			;
    -- END IF;
END;



$BODY$
LANGUAGE plpgsql;
        """
        )