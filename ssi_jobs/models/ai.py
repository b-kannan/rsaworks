# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class AI(models.Model):
    _inherit = 'account.invoice'

    ssi_job_id = fields.Many2one(
        'ssi_jobs', string='Job')
