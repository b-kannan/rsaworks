# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Prod(models.Model):
    _inherit = 'mrp.production'

    ssi_job_id = fields.Many2one(
        'ssi_jobs', string='Job')
