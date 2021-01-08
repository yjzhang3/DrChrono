from django.shortcuts import render
from django.http import HttpResponse
from drchrono_webapp.models import PatientInformation, DoctorInformation

# USE .ENV FILE FOR API TOKENS AND KEYS

import requests, json, datetime, pytz, subprocess, sys, urllib3
urllib3.disable_warnings()

API_PATIENTS = 'https://app.drchrono.com/api/patients'
API_DOCTOR = 'https://app.drchrono.com/api/doctors'

CLIENT_ID = 'BjMyUxjjeZSDy61Y1ZdGBdhVch2yCSLv5w4fY4ae'
CLIENT_SECRET = 'BGcAyd56sLYmr87v8IS1UrIZMn2fIK7ma9AIAiRX0Wo93Um2WIB1IdDZZ9OOZAjXkUKlBNahZL0qZgmAju0gHJVc4GwdZpcnR55Fd5ujraA4liBJehNwhWKmLLbOOiZD'

ACCESS_TOKEN_REN = 'deSRmIZ7Ece3ZfamL6PfOCj5CAYjI0'
REFRESH_TOKEN_REN = 't2GzQlaQpXMCwEHrfUrcOMczf6eeLk'

def make_request(url, access_token):
	print("make_request called")
	api_call_headers = {'Authorization': 'Bearer ' + access_token}
	api_call_response = requests.get(url, headers=api_call_headers, verify=False)
	# api_json = api_call_response.json()
	api_json = api_call_response.json()
	return api_json
	# if api_json:
	# 	print("make_request finished:	Not Empty")
	# 	return api_json
	# else:
	# 	print("make_request finished:	Empty")
	# 	return {}

def login_page(request, ):
    response = render(request, "login_page.html")
    return response

# figure out how to handle incorrect or timed out logins from API authentication
# request.method == 'POST' for when using Django-OAuth 2.0
def home_page(request):
	request_p = request.build_absolute_uri()
	splitted = request_p.split('code=')
	print()
	print("------------splitted: ", splitted)
	code = splitted[1]
	response = requests.post('https://drchrono.com/o/token/', data={
    		'code': code,
    		'grant_type': 'authorization_code',
    		'redirect_uri': 'http://127.0.0.1:8000/drchrono_webapp/home',
    		'client_id': CLIENT_ID,
    		'client_secret': CLIENT_SECRET,
	})
	response.raise_for_status()
	data = response.json()

	# Save these in your database associated with the user
	access_token = data['access_token']
	refresh_token = data['refresh_token']
	print("ACCESS TOKEN: ", access_token)
	print("REFRESH TOKEN: ", refresh_token)
	expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
	print('---------CODE: ', code)
	print('---------DATA: ', data)
	
	# connect api call data to data models
	json_res = make_request(API_DOCTOR, ACCESS_TOKEN_REN) # --!
	print(json_res)
	doctor, new_doc_obj = DoctorInformation.objects.update_or_create(
		doctor_id=json_res['results'][0]['id'],
		doctor_first_name=json_res['results'][0]['first_name'],
		doctor_last_name=json_res['results'][0]['last_name'],
		doctor_data_json=json_res['results'][0]
		)
	doctor.save()
	print("DOCTOR INFO: ", doctor)
	
	json_res = make_request(API_PATIENTS, ACCESS_TOKEN_REN) # --!
	for i in range(len(json_res['results'])):
		print('PATIENT ', i)
		for key, value in json_res['results'][i].items():
			print(key, ":", value)
		patient, new_pat_obj = PatientInformation.objects.update_or_create(
			patient_data_json=i,
		)

	if code:
		response = render(request, "home.html", {"user":doctor})
	else:
		response = render(request, "login_fail.html")
	return response
