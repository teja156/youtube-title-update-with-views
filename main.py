import os
import flask
import requests
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from updatetitle import start
import threading

import get_video_info
import json
import ast
import smtplib


CLIENT_SECRETS_FILE = ["client_secret_techraj1.json","client_secret_techraj2.json","client_secret_techraj3.json",
"client_secret_techraj4.json","client_secret_techraj5.json","client_secret_techraj6.json",
"client_secret_techraj7.json","client_secret_techraj8.json"]


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
NUM = 0
STARTED = False
all_credentials = []

app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def home():
	global all_credentials
	if os.path.exists("credentials.txt"):
		try:
			f = open("credentials.txt")
			all_credentials =  ast.literal_eval(f.read())
			f.close()
			print("file read")
		except:
			all_credentials = []
	else:
		all_credentials = []

	NUM = len(all_credentials)
	flask.session['NUM'] = NUM
	print("NUM init in / - ",NUM)
	return "Hi. Started = %s,NUM=%d"%(str(STARTED),NUM)

@app.route('/test')
def test():
	global NUM
	global STARTED
	global all_credentials
	NUM = flask.session['NUM']

	#NUM = len(flask.session['credentials'][0])
	#print("NUM value - %d"%NUM)

	if(NUM<8):
		return "Only %d Apps are authorized "%(NUM)
	if(STARTED):
		return "Already started"

	try:
		f = open("credentials.txt")
		all_credentials =  ast.literal_eval(f.read())
		f.close()
		print("file read")
	except:
		return "Error - No credentials.txt"

	

	t = threading.Thread(target=start,args=(all_credentials,))
	#updatetitle.start(youtube)
	t.daemon = True
	t.start()
	STARTED = True

	#All apps are authorized, so start the script
	#updatetitle(flask.session['credentials'])
	return "Started script"


@app.route('/authorize')
def authorize():
	global NUM
	global all_credentials
	NUM = flask.session['NUM']

	if(NUM==8):
		return "All 8 apps are authorized."

	print("Authorizing app %d"%(NUM+1))

	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	    CLIENT_SECRETS_FILE[NUM],
	    ['https://www.googleapis.com/auth/youtube.force-ssl'])
	flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

	# Generate URL for request to Google's OAuth 2.0 server.
	# Use kwargs to set optional request parameters.
	flask.session['state'] = "state%d"%NUM
	authorization_url, state = flow.authorization_url(
	    # Enable offline access so that you can refresh an access token without
	    # re-prompting the user for permission. Recommended for web server apps.
	    access_type='offline',
	    # Enable incremental authorization. Recommended as a best practice.
	    state='state%d'%NUM,
	    include_granted_scopes='true')

	return flask.redirect(authorization_url) #redirect to Google's Oauth server for consent

@app.route('/oauth2callback')
def oauth2callback():
	global NUM
	global all_credentials
	#After the consent, we are redirected to this page. We can retrieve the authorization code from here
	NUM = flask.session['NUM']

	#verify authorization code with state
	state = flask.session['state']
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	    CLIENT_SECRETS_FILE[NUM],
	    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
	    state=state)
	flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

	#use the flow.fetch_token method to exchange the authorization code in that response for an access token
	authorization_response = flask.request.url
	flow.fetch_token(authorization_response=authorization_response)

	#Now store credentials in the session
	credentials = flow.credentials
	if not 'credentials' in flask.session:
		flask.session['credentials'] = []
	#'credentials' : [credentials of first app, credentials of second app]
	
	all_credentials.append({
	    'token': credentials.token,
	    'refresh_token': credentials.refresh_token,
	    'token_uri': credentials.token_uri,
	    'client_id': credentials.client_id,
	    'client_secret': credentials.client_secret,
	    'scopes': credentials.scopes})

	#print("credentials : ",all_credentials)

	NUM+=1
	if(NUM==8):
		f = open('credentials.txt','w')
		f.write(str(all_credentials))
		f.close()
	#Now it can make requests with these credentials
	return "Succesfully authorized App %d <a href='/authorize'>Authorize</a> "%(NUM)

	#WHen is num incremeneting?




if __name__ == '__main__':
	# When running locally, disable OAuthlib's HTTPs verification.
	# ACTION ITEM for developers:
	#     When running in production *do not* leave this option enabled.
	#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

	if os.path.exists("credentials.txt"):
		try:
			f = open("credentials.txt")
			all_credentials =  ast.literal_eval(f.read())
			f.close()
			print("file read")
		except:
			all_credentials = []
	else:
		all_credentials = []

	NUM = len(all_credentials)
	print("NUM init - ",NUM)
	# Specify a hostname and port that are set as a valid redirect URI
	# for your API project in the Google API Console.
	app.run('localhost', 8080, debug=True)