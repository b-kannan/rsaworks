# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class PO(models.Model):
    _inherit = 'purchase.order'

    ssi_job_id = fields.Many2one(
        'ssi_jobs', string='Job')
