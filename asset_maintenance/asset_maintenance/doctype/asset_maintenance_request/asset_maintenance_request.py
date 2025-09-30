# Copyright (c) 2025, keerthana and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.user import get_users_with_role


class AssetMaintenanceRequest(Document):
	def after_insert(self):
		self.send_email()

	def send_email(self):
		"""Method to send email notification to Maintenance Supervisor , if the asset maintenance request is Urgent """
		if self.priority == "Urgent":
			recipients = get_users_with_role('Maintenance Supervisor')
			if recipients:
				subject = f"Urgent!! Asset Maintenance Request {self.name}"
				message = f"Asset Maintenance Request {self.name}. Please take necessary action."
				frappe.sendmail(
	                recipients = recipients,
	                subject = subject,
	                message = message,
	                delayed = False
				)
