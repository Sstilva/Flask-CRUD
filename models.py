from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ClientModel(db.Model):
	__tablename__ = 'clients'

	client_phone =db.Column(db.String(20), primary_key=True)
	client_name = db.Column(db.String(50), nullable=False)
	client_company = db.Column(db.String(50))

	def __init__(self, 
		client_phone, 
		client_name, 
		client_company):
	
		self.client_phone = client_phone
		self.client_name = client_name
		self.client_company = client_company

	def __repr__(self):
		return "{} - {}. {}".format(
			self.client_phone, 
			self.client_name, 
			self.client_company)


class RequestModel(db.Model):
	__tablename__ = 'requests'

	id = db.Column(db.Integer, primary_key=True)
	client_phone = db.Column(db.String(20), nullable=False)
	employee_phone = db.Column(db.String(20), nullable=False)
	request_type = db.Column(db.String(50))
	request_start_date = db.Column(db.DateTime)
	request_finish_date = db.Column(db.DateTime)

	def __init__(self,
		id,
		client_phone,
		employee_phone,
		request_type,
		request_start_date,
		request_finish_date):

		self.id = id
		self.client_phone = client_phone
		self.employee_phone = employee_phone
		self.request_type = request_type
		self.request_start_date = request_start_date
		self.request_finish_date = request_finish_date

	def __repr__(self):
		return "{}. {}: {} - {}".format(
			self.id, 
			self.request_type, 
			self.request_start_date, 
			self.request_finish_date)


class EmployeeModel(db.Model):
	__tablename__ = 'employees'

	employee_phone = db.Column(db.String(20), primary_key=True)
	employee_name = db.Column(db.String(50), nullable=False)
	employee_department = db.Column(db.String(50))
	employee_address = db.Column(db.String(100))

	def __init__(self,
		employee_phone,
		employee_name,
		employee_department,
		employee_address):

		self.employee_phone = employee_phone
		self.employee_name = employee_name
		self.employee_department = employee_department
		self.employee_address = employee_address

		def __repr__(self):
			return "{} - {}. {}".format(
				self.employee_phone, 
				self.employee_name, 
				self.employee_department)
			