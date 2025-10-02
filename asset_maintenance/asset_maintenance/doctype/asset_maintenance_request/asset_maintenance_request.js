// Copyright (c) 2025, keerthana and contributors
// For license information, please see license.txt

frappe.ui.form.on("Asset Maintenance Request", {
    refresh: function(frm) {
        frm.set_query("asset", function() {
            return {
                filters: {
                    custom_in_use: 1
                }
            };
        });
        if (!frm.is_new() && frm.doc.status == "Open") {
            if (frappe.user.has_role("Maintenance Supervisor")) {
                frm.add_custom_button(
                    __("Create Maintenance Task"),
                    function() {
                      frappe.call({
                            method: "asset_maintenance.asset_maintenance.doctype.asset_maintenance_request.asset_maintenance_request.create_task",
                            args: {
                                doc: frm.doc
                            },
                            callback: function(r) {
                                if (!r.exc) {
                                    frappe.msgprint(__("Task Created Successfully "));
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }
        }
    }
});
