# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Employee Advances",
    "summary": "This module will match employee advance to employee expense",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators",
    "category": "Human Resources",
    "website": "http://www.opensourceintegrators.com",
    "depends": [
        "hr_expense",
    ],
    "data": [
        "wizard/payment_view.xml",
        "views/hr_expense_view.xml"
    ],
    "installable": True,
}
