from airplane_mode.airplane_mode.doctype.airplane_ticket import airplane_ticket
import frappe
from frappe.model.document import Document

def execute():
	tickets = frappe.db.get_all("Airplane Ticket", pluck="name", filters={'seat': None})
	seatnumber = airplane_ticket.AirplaneTicket.generate_seat_number()
        
	for ticket in tickets:
		ticket_doc = frappe.get_doc("Airplane Ticket", ticket)
		ticket_doc.seat = seatnumber
		ticket_doc.save()
