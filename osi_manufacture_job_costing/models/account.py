# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields

class AnalyticAccountLine(models.Model):
    _inherit = 'account.analytic.line'

    workcenter_id = fields.Many2one('mrp.workcenter', string='Workcenter')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    workcenter_id = fields.Many2one('mrp.workcenter', string='Workcenter')

    @api.one
    def _prepare_analytic_line(self):
        result = super(AccountMoveLine, self)._prepare_analytic_line()       
        result[0].update({'workcenter_id': self.workcenter_id.id or False})
        return result
