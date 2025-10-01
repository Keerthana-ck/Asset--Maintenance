// Copyright (c) 2025, keerthana and contributors
// For license information, please see license.txt

frappe.query_reports["Asset Maintenance Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        },
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: ["", "Open", "In Progress", "In Review", "Completed"]
        }
    ]
};
