from requests_oauthlib import OAuth2Session
from constants import *
from oauth2client.client import (flow_from_clientsecrets,FlowExchangeError,Credentials)

def user_validator(name, email_id):
	if not name:
		return False, 'Please provide a user name.'
	if not email_id:
		return False, 'Please provide a email_id.'
	return True, None



def get_google_auth(state=None, token=None):
	if token:
		return OAuth2Session(CLIENT_ID, token=token)
	if state:
		return OAuth2Session(
			CLIENT_ID,
			state=state,
			redirect_uri=REDIRECT_URI,
			scope=SCOPE)
	oauth = OAuth2Session(
		CLIENT_ID,
		redirect_uri=REDIRECT_URI,
		scope=SCOPE)
	return oauth

def get_url_and_state(oauth):
	return oauth.authorization_url(AUTH_URI, access_type='offline')

def get_authorize_url(state):
	import os
	path = os.getcwd() + '/user/client_secret.json'
	flow = flow_from_clientsecrets(path, ' '.join(SCOPE))
	flow.params['access_type'] = 'offline'
	flow.params['approval_prompt'] = 'force'
	flow.params['state'] = state
	return flow.step1_get_authorize_url(REDIRECT_URI)

def exchange_code_for_creds(authorization_code):
	import os
	path = os.getcwd() + '/user/client_secret.json'
	flow = flow_from_clientsecrets(path, ' '.join(SCOPE))
	flow.redirect_uri = REDIRECT_URI
	credentials = flow.step2_exchange(authorization_code)
	credentials = credentials.to_json()
	return credentials


def get_credentials(authorization_code):
	try:
		credentials = exchange_code_for_creds(authorization_code)
		credentials = credentials.to_json()
		return True, credentials
	except Exception as e:
		return False, None