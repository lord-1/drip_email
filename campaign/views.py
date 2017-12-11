from flask import Flask, request, Blueprint, jsonify
from flask2.models import Campaign, User
import json
from constants import *
from utils import (create_campaign, schedule_mails)
campaign_app = Blueprint('campaign_app', __name__)

def print_me():
	print "print me"

from flask2.models import Campaign
@campaign_app.route('/campaign/<int:campaign_id>', methods=['GET', 'POST',
							 'DELETE', 'PUT'])
@campaign_app.route('/campaign/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def campain(campaign_id=None):
	if request.method == 'GET':
		'''
		To get the campaign from the campaign model
		'''
		if campaign_id:
			ob = Campaign.query.filter_by(id=campaign_id)
			data_list = []
			for item in ob:
				data_list.append('cool')
				return json.dumps(data_list)
				return 'THis is the data'
		else:
			data_list = []
			ob = Campaign.query.all()
			data_list.append({'a':'b'})
			return json.dumps(data_list)
			return 'ALL the data sets'

	if request.method == 'POST':
		'''
		To create a new campaign
		'''
		user_id = request.form.get('user_id')
		try:
			user = User.query.get(user_id)
		except Exception as e:
			return 'Invalid User Id'
		result = create_campaign(request.form, user_id)
		return result

	if request.method == 'DELETE':
		'''
		to delete a campaign
		'''
		if not campaign_id:
			return CAMPAIGN_ID_INVALID
		try:
			campaign_object = Result.query.get(campaign_id)
		except Exception as e:
			return CAMPAIGN_ID_INVALID
		try:
			db.session.delete(campaign_object)
		except Exception as e:
			return CAMPAIGN_DELETE_FAILURE
		return CAMPAIGN_DELETE_SUCCESS


	if request.method == 'PUT':
		'''
		to update the campaign
		'''
		from flask2.flask_app import scheduler
		schedule_mails({'user':'12c3ea42dd8e11e7aa2e7c04d0d56e10'})
		return 'we are in put method'


