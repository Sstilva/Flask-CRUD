from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ClientModel(db.Model):
	__tablename__ = 'clients'

	client_phone =db.Column(db.Integer, primary_key=True)
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