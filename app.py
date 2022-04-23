from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, ClientModel, RequestModel, EmployeeModel
from forms import ClientForm, RequestForm, EmployeeForm


# Initiating the app
app = Flask(__name__)

# Configuring the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost:5432/advert_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'many bytes'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/clients', methods=['GET', 'POST'])
def add_client():
	name = None
	form = ClientForm()
	if form.validate_on_submit():
		client_phone = form.phone.data
		client_name = form.name.data
		client_company = form.company.data	
		client = ClientModel(
			client_phone=client_phone, 
			client_name=client_name, 
			client_company=client_company)
		db.session.add(client)
		db.session.commit()
		form.phone.data = ''
		form.name.data = ''
		form.company.data = ''
		flash("Запись о клиенте успешно добавлена")
	our_clients = ClientModel.query.order_by(ClientModel.client_name).all()
	return render_template('clients.html',
		form=form,
		name=name,
		our_clients=our_clients)



@app.route('/clients/delete/<string:client_phone>')
def delete_client(client_phone):
	name = None
	form = ClientForm()
	client_to_delete = ClientModel.query.get_or_404(client_phone)
	try: 
		db.session.delete(client_to_delete)
		db.session.commit()
		flash("Запись о клиенте успешно удалена")
		our_clients = ClientModel.query.order_by(ClientModel.client_name).all()
		return render_template('clients.html',
			form=form,
			name=name,
			our_clients=our_clients)
	except:
		flash("Не удалось удалить запись о клиенте")
		return render_template('clients.html',
			form=form,
			name=name,
			our_clients=our_clients)


@app.route('/clients/update/<string:client_phone>', methods=['GET', 'POST'])
def update_client(client_phone):
	form = ClientForm()
	client_to_update = ClientModel.query.get_or_404(client_phone)
	if request.method == "POST":
		client_to_update.client_phone = request.form['phone']
		client_to_update.client_name = request.form['name']
		client_to_update.client_company = request.form['company']
		try: 
			db.session.commit()
			flash("Запись о клиенте успешно изменена")
			return render_template('client_update.html',
				form=form,
				client_to_update=client_to_update)
		except:
			flash("Не удалось изменить запись о клиенте")
			return render_template('client_update.html',
				form=form,
				client_to_update=client_to_update)
	else:
		return render_template('client_update.html',
				form=form,
				client_to_update=client_to_update,
				client_phone=client_phone)


@app.route('/requests', methods=['GET', 'POST'])
def add_request():
	name = None
	form = RequestForm()
	if form.validate_on_submit():
		id = form.id.data
		client_phone = form.client_phone.data
		employee_phone = form.employee_phone.data
		request_type = form.request_type.data
		request_start_date = form.request_start_date.data
		request_finish_date  = form.request_finish_date.data
		request = RequestModel(
			id=id,
			client_phone = client_phone,
			employee_phone = employee_phone,
			request_type = request_type,
			request_start_date = request_start_date,
			request_finish_date = request_finish_date)
		db.session.add(request)
		db.session.commit()
		form.id.data = ''
		form.client_phone.data = ''
		form.employee_phone.data = ''
		form.request_type.data = ''
		form.request_start_date.data = ''
		form.request_finish_date.data = ''
		flash("Запись о заявке успешно добавлена")
	our_requests = RequestModel.query.order_by(RequestModel.id).all()
	return render_template('requests.html',
		form=form,
		name=name,
		our_requests=our_requests)


@app.route('/requests/delete/<int:id>')
def delete_request(id):
	name = None
	form = RequestForm()
	request_to_delete = RequestModel.query.get_or_404(id)
	try: 
		db.session.delete(request_to_delete)
		db.session.commit()
		flash("Запись о заявке успешно удалена")
		our_requests = RequestModel.query.order_by(RequestModel.id).all()
		return render_template('requests.html',
			form=form,
			name=name,
			our_requests=our_requests)
	except:
		flash("Не удалось удалить запись о заявке")
		return render_template('requests.html',
			form=form,
			name=name,
			our_requests=our_requests)


@app.route('/requests/update/<int:id>', methods=['POST', 'GET'])
def update_request(id):
	form = RequestForm()
	request_to_update = RequestModel.query.get_or_404(id)
	if request.method == "POST":
		request_to_update.id = request.form['id']
		request_to_update.client_phone = request.form['client_phone']
		request_to_update.employee_phone = request.form['employee_phone']
		request_to_update.request_type = request.form['request_type']
		request_to_update.request_start_date = request.form['request_start_date']
		request_to_update.request_finish_date = request.form['request_finish_date']
		try: 
			db.session.commit()
			flash("Запись о заявке успешно изменена")
			return render_template('request_update.html',
				form=form,
				request_to_update=request_to_update)
		except:
			flash("Не удалось изменить запись о клиенте")
			return render_template('request_update.html',
				form=form,
				request_to_update=request_to_update)
	else:
		return render_template('request_update.html',
				form=form,
				request_to_update=request_to_update,
				id=id)


@app.route('/employees', methods=['POST', 'GET'])
def add_employee():
	name = None
	form = EmployeeForm()
	if form.validate_on_submit():
		employee_phone = form.employee_phone.data
		employee_name = form.employee_name.data
		employee_department = form.employee_department.data
		employee_address = form.employee_address.data
		employee = EmployeeModel(
			employee_phone=employee_phone,
			employee_name = employee_name,
			employee_department = employee_department,
			employee_address = employee_address)
		db.session.add(employee)
		db.session.commit()
		form.employee_phone.data = ''
		form.employee_name.data = ''
		form.employee_department.data = ''
		form.employee_address.data = ''
		flash("Запись о сотруднике успешно добавлена")
	our_employees = EmployeeModel.query.order_by(EmployeeModel.employee_phone).all()
	return render_template('employees.html',
		form=form,
		name=name,
		our_employees=our_employees)


@app.route('/employees/delete/<string:employee_phone>')
def delete_employee(employee_phone):
	name = None
	form = EmployeeForm()
	employee_to_delete = EmployeeModel.query.get_or_404(employee_phone)
	try: 
		db.session.delete(employee_to_delete)
		db.session.commit()
		flash("Запись о сотруднике успешно удалена")
		our_employees = EmployeeModel.query.order_by(EmployeeModel.employee_phone).all()
		return render_template('employees.html',
			form=form,
			name=name,
			our_employees=our_employees)
	except:
		flash("Не удалось удалить запись о работнике")
		return render_template('employees.html',
			form=form,
			name=name,
			our_employees=our_employees)


@app.route('/employees/update/<string:employee_phone>', methods=['POST', 'GET'])
def update_employee(employee_phone):
	form = EmployeeForm()
	employee_to_update = EmployeeModel.query.get_or_404(employee_phone)
	if request.method == "POST":
		employee_to_update.employee_phone = request.form['employee_phone']
		employee_to_update.employee_name = request.form['employee_name']
		employee_to_update.employee_department = request.form['employee_department']
		employee_to_update.employee_address = request.form['employee_address']
		try: 
			db.session.commit()
			flash("Запись о сотруднике успешно изменена")
			return render_template('employee_update.html',
				form=form,
				employee_to_update=employee_to_update)
		except:
			flash("Не удалось изменить запись о сотруднике")
			return render_template('employee_update.html',
				form=form,
				employee_to_update=employee_to_update)
	else:
		return render_template('employee_update.html',
				form=form,
				employee_to_update=employee_to_update,
				employee_phone=employee_phone)


if __name__ == "__main__":
	app.run()
