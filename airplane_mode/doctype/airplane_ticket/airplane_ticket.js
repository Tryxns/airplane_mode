// Copyright (c) 2025, Fabian Jevon and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Airplane Ticket', {
   refresh: function(frm) {
       frm.add_custom_button(__('Assign Seat'), function() {
        //    frappe.msgprint(frm.doc.email);

        let d = new frappe.ui.Dialog({
            title: 'Select seat',
            fields: [
                {
                    label: 'Seat Number',
                    fieldname: 'seat',
                    fieldtype: 'Data'
                }
            ],
            size: 'small', // small, large, extra-large 
            primary_action_label: 'Submit',
            primary_action(values) {
                console.log(values.seat);
                frm.set_value('seat', values.seat);
                d.hide();
            }
        });
        d.show();
       }, __("Actions"));
   }
});
