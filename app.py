from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, ClientModel


# Initiating the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:crimsoneyes@localhost:5432/advert_db'
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
def clients():
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
		flash("Client added")
	our_clients = ClientModel.query.order_by(ClientModel.client_name).all()
	return render_template('clients.html',
		form=form,
		name=name,
		our_clients=our_clients)

if __name__ == "__main__":
	app.run(debug=True)