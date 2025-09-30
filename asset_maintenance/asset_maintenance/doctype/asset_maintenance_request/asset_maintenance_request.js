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
    }
});
