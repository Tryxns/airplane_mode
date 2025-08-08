// Copyright (c) 2025, Fabian Jevon and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airline", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Airline', {
 refresh(frm) {
    const website_link = frm.doc.website;
    frm.add_web_link(website_link, "Visit Website");
 }
})