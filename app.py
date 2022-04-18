from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


# Initiating the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SECRET_KEY'] = 'many bytes'

db = SQLAlchemy(app)


class Client(db.Model):
	phone =db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	company = db.Column(db.String(50))

	def __repr__(self):
		return '<Name %r>' % self.name


class ClientForm(FlaskForm):
	phone = StringField("Phone", validators=[DataRequired()])
	name = StringField("Name", validators=[DataRequired()])
	company = StringField("Company", validators=[DataRequired()])
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
		client = Client(phone=client_phone, 
						name=client_name, 
						company=client_company)
		db.session.add(client)
		db.session.commit()
		form.phone.data = ''
		form.name.data = ''
		form.company.data = ''
		flash("Client added")
	our_clients = Client.query.order_by(Client.name).all()
	return render_template('clients.html',
		form=form,
		name=name,
		our_clients=our_clients)

if __name__ == "__main__":
	app.run()