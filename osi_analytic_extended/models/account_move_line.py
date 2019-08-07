# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'
    

    @api.depends('product_id')
    def _get_product_categ_id(self):
        for mline in self:
            mline.product_category_id = False
            if mline.product_id:
                mline.product_category_id = mline.product_id.categ_id and\
                    mline.product_id.categ_id.id or False

    product_category_id = fields.Many2one(
        'product.category', 'Product Category',
        compute='_get_product_categ_id', store=True)
