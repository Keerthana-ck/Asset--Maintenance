# Copyright (c) 2025, keerthana and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe.utils.user import get_users_with_role
from frappe.desk.form.assign_to import add as assign_task
from frappe import _


class AssetMaintenanceRequest(Document):
	def after_insert(self):
		self.send_email()

	def validate(self):
		self.validate_asset_maintenance_request()
		self.validate_expected_completion_date()

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

	def validate_asset_maintenance_request(self):
	    """method to Validate Asset Maintenance Request to prevent duplicate entry"""
	    overlapping = frappe.db.sql("""
	        SELECT name
	        FROM `tabAsset Maintenance Request`
	        WHERE asset = %(asset)s
	          AND status NOT IN ('Completed')
	          AND name != %(name)s
	          AND (
	                (%(request_date)s < expected_completed_date)
	                AND (%(expected_completed_date)s > request_date)
	              )
	    """, {
	        "asset": self.asset,
	        "request_date": self.request_date,
	        "expected_completed_date": self.expected_completed_date,
	        "name": self.name or "New Asset Maintenance Request"
	    }, as_dict=True)

	    if overlapping:
	        frappe.throw(
	            _("Asset {0} is already booked during this time slot").format(self.asset)
	        )

	def validate_expected_completion_date(self):
	    """Validate Requested date and Expacted Completion data"""
	    if self.request_date and self.expected_completed_date:
	        if self.expected_completed_date <= self.request_date:
	            frappe.throw(_("Expected Completion Date must be greater than Requested Dßate"))



@frappe.whitelist()
def create_task(doc):
	"""Method to Create task and auto assign it to Maintenance Team Member """
	if isinstance(doc, str):
		doc = json.loads(doc)
	doc = frappe._dict(doc)

	existing_tasks = frappe.db.count('Task', {'custom_reference_document': doc.name})
	task_number = existing_tasks + 1

	task = frappe.new_doc("Task")
	task.subject = f"{doc.asset_name} - {doc.maintenance_type} - {int(task_number):03d}"
	task.priority = doc.priority
	task.custom_asset = doc.asset
	task.custom_requested_by = doc.requested_by
	task.custom_maintenance_type = doc.maintenance_type
	task.exp_start_date = doc.request_date
	task.exp_end_date = doc.expected_completed_date
	task.expected_time = doc.resolution_time
	task.custom_reference_document = doc.name
	task.insert(ignore_permissions=True)

	members = frappe.get_all(
        "Has Role", filters={"role": "Maintenance Team member"}, fields=["parent"]
	)
	if members:
		member = members[0].parent
		assign_task({
            "assign_to": [member],
            "doctype": "Task",
            "name": task.name,
            "description": f"Assigned by Maintenance Supervisor for Asset {doc.asset}"
		})

	frappe.db.set_value("Asset Maintenance Request", doc.name, "status", "In Progress")

	return task.name
