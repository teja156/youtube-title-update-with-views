import get_video_info
import json
import time
import smtplib
import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

VIDEO_ID = os.getenv("VIDEO_ID")
FREQUENCY = int(os.getenv("FREQUENCY"))
#MAIL_PASSWORD = "Test"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def fillForm(message):
	#Write errors to google form
	field_name = os.getenv("field_name")
	form_id = os.getenv("form_id")
	url = "https://docs.google.com/forms/d/e/%s/formResponse?%s=%s"%(form_id,field_name,message)
	r = requests.post(url)
	#print(r.text)

def credentials_to_dict(credentials):
	return {'token': credentials.token,
	  'refresh_token': credentials.refresh_token,
	  'token_uri': credentials.token_uri,
	  'client_id': credentials.client_id,
	  'client_secret': credentials.client_secret,
	  'scopes': credentials.scopes}


def make_title(comments,views,likes):
	TEMPLATE = "This video has %s views and %s likes"%(views,likes)
	return TEMPLATE

def start(flask_credentials):
	print("STARTED")
	tags = ["tech raj","tom scott","youtube title update views","show views in youtube title","youtube data api","v3","api","application program interface"]
	num = 0
	while True:
		time.sleep(FREQUENCY) #60 seconds
		info = get_video_info.getinfo()
		updated_title = make_title(info['comments'],info['views'],info['likes'])


		if(info['title'].strip()==updated_title.strip()):
			#nothing to change
			continue

		# Load credentials from the session.
		print("Using App : %d"%(num+1))
		#print(flask_credentials)

		try:
			credentials = google.oauth2.credentials.Credentials(**flask_credentials[num])
			youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
			#flask.session['credentials'] = credentials_to_dict(credentials)

			youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
			#flask.session['credentials'][num] = credentials_to_dict(credentials)

			request = youtube.videos().update(
				part="snippet",
		        body={
		          "id": VIDEO_ID,
		          "snippet": {
		            "categoryId": 22,
		            "defaultLanguage": "en",
		            "title": updated_title,
		            "description": info['description'],
		            "tags" : tags
		          },

		        })

			response = request.execute()
			#print(response)
			if "error" in response:
				#Some error occured, notify via mail
				try:
					fillForm(str(response))
				except:
					pass
		except Exception as e:
			try:
				fillForm(str(e))
			except:
				pass

		num+=1
		if(num==8):
			num = 0


			

