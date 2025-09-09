# -*- coding: utf-8 -*-
from odoo import models, fields

class DjbcCategs(models.Model):
    _name = 'djbc.categs'
    _description = 'DJBC Categories'
    _rec_name = 'name'

    name = fields.Char(string='DJBC Category', required=True)