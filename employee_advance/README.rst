.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Employee Advances
=================

This module will reconcile the existing advance against the expense from the
expense form.

Test Scenario
=============

* Create a new Payment via the Accounting module. 
* Select the Travel Advance journal, and include a memo such as Travel Advance.
* Validate the payment.
* Create a new expense.
* Submit to Manager (makes a report for the expense)
* Approve the report and Post Journal Entries.
* Click the “Register Payment” button
* Review if there are existing advances for the associated employee
* If an advance exists, apply the payment to the expense.
* Reconcile the expense and the payment
* If a balance is due to the employee, register another payment and validate
* If a balance is due back to company, decide whether to leave the open
  balance with the employee or whether to receive payment back from the
  employee.


Credits
=======
Open Source Integrators

Contributors
------------

* Balaji Kannan <bkannan@opensourceintegrators.com>
* Bhavesh Odedra <bodedra@opensourceintegrators.com>
