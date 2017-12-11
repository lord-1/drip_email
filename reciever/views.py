from flask import Flask, request, Blueprint, jsonify
from flask2.models import Reciever
from flask2.flask_app import db
import json

reciever_app = Blueprint('reciever_app', __name__)

@reciever_app.route('/reciever/<int:reciever_id>', methods=['GET', 'POST',
							 'DELETE', 'PUT'])
@reciever_app.route('/reciever/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def reciever(reciever_id=None):
	if request.method == 'GET':
		return 'get was called'
	if request.method == 'POST':
		name = request.form.get('name', '')
		if not name:
			return 'Please provide a name'
		email_address = request.form.get('email', '')
		if not email_address:
			return 'Please provide an email_address.'
		r = Reciever(name=name, email_id=email_address)
		db.session.add(r)
		db.session.commit()
		return 'The reciver was stored.'
	if request.method == 'DELETE':
		return 'DELETE'
	if reques.method == 'PUT':
		return 'put'
