from constants import *
from flask2.models import *
import ast
import datetime
from oauth2client import client
from apiclient import discovery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import httplib2
from flask2.flask_app import scheduler


def build_service(user):

	user_object = User.query.get(user)
	creds = client.OAuth2Credentials.from_json(
								user_object.credentials)
	http = creds.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	return service


def create_message(data_dict):
	msg = MIMEMultipart('alternative')
	msg['subject'] = 'Successfully messsaged'
	msg['from'] = 'sandeep.hukku93@gmail.com'
	msg['From'] = 'sandeep.hukku93@gmail.com'
	msg['To'] = 'sandeep.hukku@happay.in'
	return {'raw': base64.urlsafe_b64encode(msg.as_string())}


def send_message(user, raw_data):
	service = build_service(user)
	try:
		service.users().messages().send(userId="me", body=raw_data).execute()
	except Exception as e:
		print 'Failed to mail'


def schedule_mails(item_data):
	import pdb
	pdb.set_trace()
	job_id = None
	user = item_data['user']
	raw_message = create_message(item_data)
	from flask2.flask_app import scheduler
	scheduler.add_job(send_message, 'interval', [user, raw_message], seconds=15, id='this is the test')
	print "this is done"
	'''
	now we get the ids of the users to whom the mail needs to be sent
	'''

	#write the function to send the mail over here
	return job_id


def validate_params(day_flow, mail_info, user):
	"""Summary
	
	Args:
	    day_flow (string): day flow for the campaign
	    mail_info (TYPE): to whom the mail is to be sent.
	
	Returns:
	    bool, string, (None, json), (None, json): return if the
	    mail_info and the day_flow is correct, if yes then returns 
	    success, success string and the jsonified objects of the two 
	    strings
	"""
	mail_info = ast.literal_eval(mail_info)
	day_flow = ast.literal_eval(day_flow)
	if day_flow == {} or mail_info == {}:
		return False, EMPTY_VALUE_ERROR, None, None

	day_flow_keys = day_flow.keys()
	for item in day_flow_keys:
		if not isinstance(item, int):
			return False, DAY_TYPE_ERROR, None, None
		single_flow_dict = day_flow[item]
		if not single_flow_dict.get('time', None):
			return False, 'Invalid time', None, None
		try:
			import pdb
			pdb.set_trace()
			hours, minutes, seconds = map(int, 
							day_flow[item]['time'].split(':'))
			start_time = datetime.datetime(year=2017, month=10, day=12,
						hour=hours, minute=minutes, second=seconds)
			day_flow_item = day_flow[item]
			day_flow_item["time"] =  str(start_time)
			day_flow[item] = day_flow_item
		except Exception as e:
			return False, 'Invalid Time', None, None

	if not mail_info.get('to', None):
		return False, TO_MAIL_ERROR, None, None
	if not mail_info.get('subject', None):
		return False, SUBJECT_MISS_ERROR, None, None
	import pdb
	pdb.set_trace()
	return True, 'Success', day_flow, mail_info


def create_campaign(data_dict, user):
	"""Summary
	
	Args:
	    data_dict (json): the form object from request
	
	Returns:
	    string: String of the result
	"""
	campaign_name = data_dict.get('campaign_name', None)
	if not campaign_name or len(campaign_name) > 200:
		return CAMPAIGN_NAME_ERROR
	day_flow = data_dict.get('day_flow', '{}')
	mail_info = data_dict.get('mail_info', '{}')
	success, res_str, day_flow, mail_info = validate_params(
								day_flow, mail_info, user)
	if not success:
		return res_str
	campaign_object = Campaign(campaign_name=campaign_name,
					day_flow=day_flow, mail_info=mail_info,
					user=user)
	try:
		db.session.add(campaign_object)
		db.session.commit()
		return CAMPAIGN_SAVE_SUCCESS
	except Exception as e:
		return CAMPAIGN_SAVE_FAILURE


def validate_users(user_li):
	valid_users, invalid_users = [], []
	for item in user_li:
		try:
			user = Reciever.query.get(int(item))
			valid_users.append(item)
		except Exception as e:
			invalid_users.append(item)
		return valid_users, invalid_users

def validate_campaign(campaign_id):
	if not campaign_id:
		return False, 'Invalid campaign Id', None
	try:
		campaign_id = int(campaign_id)
	except Exception as e:
		return False, 'Invalid camapaign Id', None
	try:
		campaign = Campaign.query.get(campaign_id)
		return True, None, campaign
	except Exception as e:
		return False, 'Unknonwn Campaign Id', None





