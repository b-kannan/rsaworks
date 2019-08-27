# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import requests


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'
    
#     equip_id = fields.Char(string='Equip_id')
    storage_id = fields.One2many('storage', 'subscription_id', string='Storage')
