from django.shortcuts import render
from django.http import HttpResponse
from drchrono_webapp.models import PatientInformation, DoctorInformation

# USE .ENV FILE FOR API TOKENS AND KEYS

import datetime, pytz, requests

def login_page(request, ):
    response = render(request, "login_page.html")
    return response

# figure out how to handle incorrect or timed out logins from API authentication
# request.method == 'POST' for when using OAuth 2.0
def home_page(request):
	request_p = request.build_absolute_uri()
	splitted = request_p.split('code=')
	code = splitted[1]
	response = requests.post('https://drchrono.com/o/token/', data={
    		'code': code,
    		'grant_type': 'authorization_code',
    		'redirect_uri': 'http://127.0.0.1:8000/drchrono_webapp/home',
    		'client_id': 'BjMyUxjjeZSDy61Y1ZdGBdhVch2yCSLv5w4fY4ae',
    		'client_secret': 'BGcAyd56sLYmr87v8IS1UrIZMn2fIK7ma9AIAiRX0Wo93Um2WIB1IdDZZ9OOZAjXkUKlBNahZL0qZgmAju0gHJVc4GwdZpcnR55Fd5ujraA4liBJehNwhWKmLLbOOiZD',
	})
	response.raise_for_status()
	data = response.json()

	# Save these in your database associated with the user
	access_token = data['access_token']
	refresh_token = data['refresh_token']
	expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
	print('---------CODE: ', code)
	print('---------DATA: ', data)
	if code:
        	response = render(request, "home.html")
	else:
        	response = render(request, "login_fail.html")
	return response
