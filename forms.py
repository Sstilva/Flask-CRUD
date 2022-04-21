from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClientForm(FlaskForm):
	phone = StringField("Phone", validators=[DataRequired()])
	name = StringField("Name", validators=[DataRequired()])
	company = StringField("Company")
	submit = SubmitField("Submit")


class RequestForm(FlaskForm):
	id = StringField("ID", validators=[DataRequired()])
	client_phone = StringField("Client phone", validators=[DataRequired()])
	employee_phone = StringField("Employee phone", validators=[DataRequired()])
	request_type = StringField("Request type", validators=[DataRequired()])
	request_start_date = StringField("Start date")
	request_finish_date = StringField("Finish date")
	submit = SubmitField("Submit")


class EmployeeForm(FlaskForm):
	employee_phone = StringField("Phone", validators=[DataRequired()])
	employee_name = StringField("Name", validators=[DataRequired()])
	employee_department = StringField("Department", validators=[DataRequired()])
	employee_address = StringField("Address")
	submit = SubmitField("Submit")
