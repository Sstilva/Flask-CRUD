from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, ClientModel


# Initiating the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@localhost:5432/advert_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'many bytes'
db.init_app(app)
migrate = Migrate(app, db)


class ClientForm(FlaskForm):
	phone = StringField("Phone", validators=[DataRequired()])
	name = StringField("Name", validators=[DataRequired()])
	company = StringField("Company")
	submit = SubmitField("Submit")
	edit = SubmitField("Edit")
	delete = SubmitField("Delete")


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


if __name__ == "__main__":
	app.run()
