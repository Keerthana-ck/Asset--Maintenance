import frappe
from frappe.utils import get_datetime


@frappe.whitelist()
def update_asset_maintenance_request(doc, method = None):
    """Method to Calculate the resolution time and change status to
    In Review of the Asset Maintenance Request when the task is Completes"""
    if doc.status == "Completed" and doc.custom_reference_document:
        maintenance_doc = frappe.get_doc("Asset Maintenance Request", doc.custom_reference_document)
        if maintenance_doc.request_date and doc.completed_on:
            start = get_datetime(maintenance_doc.request_date)
            end = get_datetime(doc.completed_on)
            resolution_hours = (end - start).total_seconds() / 3600

            maintenance_doc.completed_date = doc.completed_on
            maintenance_doc.resolution_time = resolution_hours
            maintenance_doc.status = "In Review"
            maintenance_doc.save(ignore_permissions=True)
            frappe.db.commit()
