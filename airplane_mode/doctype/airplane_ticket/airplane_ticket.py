# Copyright (c) 2025, Fabian Jevon and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):
	@staticmethod
	def generate_seat_number():
		random_number = random.randint(1, 99)
		random_letter = chr(random.randint(ord('A'), ord('E')))
		return f'{str(random_number)}{random_letter}'

	def before_save(self):
		sum_add_ons = 0
		if self.add_ons:
			for item in self.add_ons:
				sum_add_ons += item.amount

		self.total_amount = int(self.flight_price) + sum_add_ons

	def validate(self):
		items = []
		for item in self.add_ons:
			if item.item in items:
				(self.add_ons).remove(item)
			else:
				items.append(item.item)
		
		total_passenger = frappe.db.count('Airplane Ticket', {'flight': self.flight})
		airplane = frappe.db.get_value('Airplane Flight', self.flight, 'airplane')
		airplane_cap = frappe.db.get_value('Airplane', airplane, 'capacity')

		if total_passenger >= airplane_cap:
			frappe.throw("This flight is full")
		
	def before_submit(self):
		if self.status != 'Boarded':
			frappe.throw("This passenger is not boarded yet")

	def before_insert(self):
		self.seat = self.generate_seat_number()