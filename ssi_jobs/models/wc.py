# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class WC(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    ssi_job_id = fields.Many2one('ssi_jobs', related='workorder_id.ssi_job_id', string='Job', readonly=True, store=False)
	company_partner_id = fields.Many2one('res.partner', related='company_id.partner_id', string='Account Holder', readonly=True, store=False)
#    ssi_job_id = fields.Many2one(
#        'workorder_id.ssi_job_id', string='Job')
    # ssi_job_id = fields.Many2one(
    #     related='workorder_id.ssi_job_id', relation="ssi_jobs.ssi_jobs", string='Job', domain=[])
