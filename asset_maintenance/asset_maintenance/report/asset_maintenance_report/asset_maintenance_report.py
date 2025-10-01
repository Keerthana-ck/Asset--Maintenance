# Copyright (c) 2025, keerthana and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "ID", "fieldname": "name", "fieldtype": "Link", "options": "Asset Maintenance Request", "width": 150},
        {"label": "Asset", "fieldname": "asset", "fieldtype": "Link", "options": "Asset", "width": 150},
        {"label": "Asset Name", "fieldname": "asset_name", "fieldtype": "Data", "width": 150},
        {"label": "Maintenance Type", "fieldname": "maintenance_type", "fieldtype": "Data", "width": 150},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": "Requested By", "fieldname": "requested_by", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
        {"label": "Request Date", "fieldname": "request_date", "fieldtype": "Date", "width": 120},
        {"label": "Expected Completed Date", "fieldname": "expected_completed_date", "fieldtype": "Date", "width": 120},
        {"label": "Completed Date", "fieldname": "completed_date", "fieldtype": "Date", "width": 120},
        {"label": "Resolution Time", "fieldname": "resolution_time", "fieldtype": "Int", "width": 150},
    ]


def get_data(filters):
    conditions = []
    values = {}

    if filters.get("from_date"):
        conditions.append("request_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("expected_completed_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters["status"]

    condition_sql = " AND ".join(conditions)
    if condition_sql:
        condition_sql = "WHERE " + condition_sql

    query = f"""
        SELECT
            name,
            asset,
            asset_name,
            maintenance_type,
            priority,
            status,
            requested_by,
            employee_name,
            request_date,
            expected_completed_date,
            completed_date,
            resolution_time
        FROM `tabAsset Maintenance Request`
        {condition_sql}
        ORDER BY request_date DESC
    """

    return frappe.db.sql(query, values, as_dict=True)
