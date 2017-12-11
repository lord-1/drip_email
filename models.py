from sqlalchemy.dialects.postgresql import JSON
from flask_app import db

class Campaign(db.Model):
	__tablename__ = 'campaigns'

	id = db.Column(db.Integer, primary_key=True)
	campaign_name = db.Column(db.String(100), unique=True, nullable=False)
	day_flow = db.Column(JSON)
	mail_info = db.Column(JSON)
	user = db.Column(db.String, db.ForeignKey('user.id') )

	def __init__(self, campaign_name, day_flow, mail_info, user):
		self.campaign_name = campaign_name
		self.day_flow = day_flow
		self.mail_info = mail_info
		self.user = user

	def serializer(self):
		return self.campaign_name
	

class Result(db.Model):
	__tablename__ = 'results_2'

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String())
	result_all = db.Column(JSON)
	result_no_stop_words = db.Column(JSON)

	def __init__(self, url, result_all, result_no_stop_words):
		self.url = url
		self.result_all = result_all
		self.result_no_stop_words = result_no_stop_words

	def __repr__(self):
		return '<id {}>'.format(self.id)

class Reciever(db.Model):
	__tablename__ = 'reciever'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email_id = db.Column(db.String(100), nullable=False)

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.String, primary_key=True)
	user_name = db.Column(db.String(200), nullable=False)
	email_id = db.Column(db.String(100), nullable=False)
	tokens = db.Column(db.Text, nullable=True)
	credentials = db.Column(JSON, nullable=True)
	campaigns = db.relationship('Campaign', backref='campaigns', lazy='dynamic')