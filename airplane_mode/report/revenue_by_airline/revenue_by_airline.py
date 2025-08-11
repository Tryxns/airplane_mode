# Copyright (c) 2025, Fabian Jevon and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Sum

def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()
	final_revenue = sum([x.total_revenue for x in data])
	
	chart = {
		'data': {
			'labels': [x.airline for x in data],
			'datasets': [
				{'values': [x.total_revenue for x in data]}
			]
		},
		'type': 'donut'
	}

	summary = [{
		"value": final_revenue,
		"indicator": "Green" if final_revenue > 0 else "Red",
		"label": _("Total Revenue"),
		"datatype": "Currency",
		"currency": "IDR"
	}]

	return columns, data, None, chart, summary
	# return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline"
		},
		{
			"label": _("Revenue"),
			"fieldname": "total_revenue",
			"fieldtype": "Currency",
		},
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""

	# frappe.qb.from_('Airplane Ticket').select(
	# 	'id', 'fname', 'lname', 'phone'
	# 	).run()

	ticket = frappe.qb.DocType('Airplane Ticket')
	flight = frappe.qb.DocType('Airplane Flight')
	airplane = frappe.qb.DocType('Airplane')
	sum_amount = Sum(ticket.total_amount).as_("total_revenue")


	# result = frappe.db.sql(
	# 	f"""
	# 	SELECT SUM(total_amount) as total_revenue, airline
	# 	FROM `tabAirplane Ticket` as ticket
	# 	INNER JOIN `tabAirplane Flight` as flight on ticket.flight = flight.name
	# 	INNER JOIN `tabAirplane` as airplane on flight.airplane = airplane.name
	# 	Group By airplane.airline
	# 	"""
	# )
	# print(result)

	query_str = (frappe.qb.from_(ticket)
	.inner_join(flight)
	.on(ticket.flight == flight.name)
	.inner_join(airplane)
	.on(flight.airplane == airplane.name)
	.select(sum_amount, airplane.airline)
	.groupby(airplane.airline))
	# print(query_str)
	
	result = query_str.run(as_dict=True)
	print(result)
	# tickets = frappe.get_all("Airplane Ticket", fields=["SUM(total_amount) as total_revenue", "flight.airplane as airplane"], group_by="airplane")

	# for ticket in tickets:
	# 	ticket.airline = frappe.db.get_value('Airplane', ticket.airplane, 'airline')
	# 	del ticket['airplane']

	return result
