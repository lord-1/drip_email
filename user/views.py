from flask import Flask, request, Blueprint, jsonify
from flask2.models import User
from flask2.flask_app import db
from utils import (get_google_auth, get_url_and_state,
						exchange_code_for_creds, get_authorize_url,
						user_validator)
import json
import uuid

user_app = Blueprint('user_app', __name__)

@user_app.route('/create', methods=['POST',
					'DELETE', 'PUT'])
def create_user():
	if request.method == 'POST':
		name = request.form.get('name', None)
		email_id = request.form.get('email_id', None)
		user_id = str(uuid.uuid1()).replace('-', '')
		success, res_str = user_validator(name, email_id)
		if not success:
			return res_str
		user = User(user_name=name, email_id=email_id, id=user_id)
		db.session.add(user)
		db.session.commit()
		return 'THe user was updated in the db.'


@user_app.route('/delete', methods=['POST',
					'DELETE', 'PUT'])
def delete_user():
	if request.method == 'DELETE':
		user_id = request.form.get('user_id', None)
		if not user_id:
			return 'Please provide a user_id'
		user = None
		try:
			user = User.query.get(user_id)
		except Exception as e:
			return 'No such user exists.'
		db.session.delete(user)
		db.session.commit()
		return 'The user was successfully deleted.'


@user_app.route('/user/<int:user_id>', methods=['GET', 'POST',
							 'DELETE', 'PUT'])
@user_app.route('/user/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def get_auth_url(user_id=None):
	if request.method == 'GET':
		if not user_id:
			return 'Please provide a user Id.'

	if request.method == 'POST':
		user_id = request.form.get('user_id')
		try:
			auth_url= get_authorize_url(state=user_id)
		except Exception as e:
			return 'Unable to generate Auth URL'
	return auth_url


@user_app.route('/creds', methods=['GET', 'POST',
							 'DELETE', 'PUT'])
def get_creds():
	auth_code = request.args.get('code')
	state = request.args.get('state')
	if not auth_code:
		return 'Authorization failed'
	if not state:
		return 'User Id was not specified.'
	credentials = None
	try:
		credentials = exchange_code_for_creds(auth_code)
	except Exception as e:
		return 'We were unable to fetch the credentials.'
	user = User.query.get(state)
	user.credentials = credentials
	db.session.commit()
	return "Your credentials are updated"


