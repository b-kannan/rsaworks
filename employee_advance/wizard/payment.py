# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from werkzeug import url_encode


class HrExpenseRegisterPaymentWizard(models.TransientModel):
    _inherit = 'hr.expense.sheet.register.payment.wizard'

    wizard_line = fields.One2many(
        'hr.expense.sheet.register.payment.wizard.line',
        'wizard_id',
        string="Payment Reconcile Line",
    )
    amount_to_reconcile = fields.Float(string="Amount Remaining to Reconcile")

    @api.onchange('wizard_line', 'amount')
    def onchange_wizard_line(self):
        if self.wizard_line:
            amount = 0.0
            for line in self.wizard_line.filtered(lambda x: x.is_select):
                amount += line.amount_to_reconcile
            self.amount_to_reconcile = self.amount - amount

    @api.model
    def default_get(self, fields):
        res = super(HrExpenseRegisterPaymentWizard, self).default_get(fields)
        move_line_pool = self.env['account.move.line']
        partner_pool = self.env['res.partner']
        partner = partner_pool.browse(res.get('partner_id'))
        accounting_parnter = partner_pool._find_accounting_partner(partner).id
        domain = [('partner_id', '=', accounting_parnter),
                  ('account_id', '=', partner.property_account_payable_id.id),
                  ('reconciled', '=', False),
                  '|',
                  ('amount_residual', '!=', 0.0),
                  ('amount_residual_currency', '!=', 0.0),
                  ('credit', '=', 0),
                  ('debit', '>', 0)]
        lines = move_line_pool.search(domain)
        res.update({'amount_to_reconcile': res.get('amount')})
        if lines:
            wizard_line = []
            for line in lines:
                vals = {'move_line_id': line.id,
                        'payment_name': line.name,
                        'partner_id': res.get('partner_id'),
                        'memo': line.ref,
                        'balance': abs(line.amount_residual),
                        'balance_info': abs(line.amount_residual),
                        'payment_date': line.date,
                        'paid_amount': line.debit}
                wizard_line.append((0,0, vals))
            if wizard_line:
                res.update({'wizard_line': wizard_line})
        return res

    def _get_payment_vals(self):
        res = super(HrExpenseRegisterPaymentWizard, self)._get_payment_vals()
        context = dict(self._context or {})
        if 'amount_to_reconcile' in context:
            res.update({'amount': context.get('amount_to_reconcile')})
        return res

    @api.multi
    def create_validate_payment(self):
        self.ensure_one()

        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        expense_sheet = self.env['hr.expense.sheet'].browse(active_ids)
        move_line_ids = []

        if self.amount_to_reconcile < 0.0:
            raise ValidationError(_('You cannot reconcile with over amount!'))

        for line in self.wizard_line.filtered(lambda x: x.is_select):
            if line.amount_to_reconcile <= 0.0:
                raise ValidationError(_('You cannot reconcile with amount '
                                        '0.0!'))
            elif line.balance_info < line.amount_to_reconcile:
                raise ValidationError(_('You can reconcile payment upto %s!'
                                        '' % line.balance_info))
            else:
                # Fetch payment from move line
                payment = line.move_line_id.payment_id

                # Log the payment in the chatter
                body = (_("A payment of %s %s with the reference "
                          "<a href='/mail/view?%s'>%s</a> related to your "
                          "expense %s has been made.") % (
                            line.amount_to_reconcile,
                            payment.currency_id.symbol,
                            url_encode({'model': 'account.payment',
                                        'res_id': payment.id}),
                            payment.name, expense_sheet.name))
                expense_sheet.message_post(body=body)
                move_line_ids += payment.move_line_ids.ids

        if move_line_ids:
            # Check remaining amount to reconcile
            if self.amount_to_reconcile > 0.0:

                # Create payment and post it
                context.update({
                    'amount_to_reconcile': self.amount_to_reconcile})
                values = self.with_context(context)._get_payment_vals()
                payment = self.env['account.payment'].create(values)
                payment.post()

                # Log the payment in the chatter
                body = (_("A payment of %s %s with the reference "
                          "<a href='/mail/view?%s'>%s</a> related to your "
                          "expense %s has been made.") % (
                            payment.amount,
                            payment.currency_id.symbol,
                            url_encode({'model': 'account.payment',
                                        'res_id': payment.id}),
                            payment.name, expense_sheet.name))
                expense_sheet.message_post(body=body)
                move_line_ids += payment.move_line_ids.ids

            # Reconcile the payment and the expense
            account_move_lines_to_reconcile = self.env['account.move.line']
            move_line_ids = account_move_lines_to_reconcile.browse(
                move_line_ids)
            lines = (move_line_ids +
                     expense_sheet.account_move_id.line_ids)
            for line in lines:
                if line.account_id.internal_type == 'payable':
                    account_move_lines_to_reconcile |= line
            account_move_lines_to_reconcile.reconcile()
        return True


class HrExpenseRegisterPaymentWizardLine(models.TransientModel):
    _name = 'hr.expense.sheet.register.payment.wizard.line'
    _description = "Expense Report Register Payment wizard line"

    wizard_id = fields.Many2one('hr.expense.sheet.register.payment.wizard')
    move_line_id = fields.Many2one('account.move.line')
    balance = fields.Float(string="Balance", readonly="1")
    balance_info = fields.Float(string="Balance")
    payment_name = fields.Char(string="Payment", readonly="1")
    partner_id = fields.Many2one('res.partner', string="Partner", readonly="1")
    memo = fields.Char(string="Memo", readonly="1")
    payment_date = fields.Date(string="Date", readonly="1", store=True)
    paid_amount = fields.Float(string="Amount", readonly="1")
    amount_to_reconcile = fields.Float(string="Amount to Reconcile")
    is_select = fields.Boolean(string="Is Selected?")
