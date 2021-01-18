from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from drchrono_webapp.models import PatientInformation, DoctorInformation
import os
from dotenv import load_dotenv
import requests, json, datetime, pytz, subprocess, sys, urllib3
urllib3.disable_warnings()
load_dotenv()

# API_PATIENTS = os.getenv('API_PATIENTS')
# API_DOCTOR = os.getenv('API_DOCTOR')
# CLIENT_ID = os.getenv('CLIENT_ID')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET')

API_PATIENTS = 'https://app.drchrono.com/api/patients'
API_DOCTOR = 'https://app.drchrono.com/api/doctors'
CLIENT_ID = 'gCVCP45fvAZqwlQvB6d4CUqEFlonrXTCjbr90BLm'
CLIENT_SECRET = 'ZvfvYGFNkabOPiLhQYlxacUWS8c1mA6Sc8Ec0XEaPhaYBCXMy1l89qyXDqMA8XbAQCHmnfuEf6BchB9WGBaeTTkpRe4B7Y9HlJVbAIR1NLVmkpwXQ3b0Vh3ax1LIQM3R'
REDIRECT_URI = 'https://drdash.herokuapp.com/'
# REDIRECT_URI = 'http://127.0.0.1:8000/'

def make_request(url, access_token):
	print("make_request called")
	api_call_headers = {'Authorization': 'Bearer ' + access_token}
	api_call_response = requests.get(url, headers=api_call_headers, verify=False)
	# api_json = api_call_response.json()
	print('------------Response Code', api_call_response)
	api_json = api_call_response.json()
	return api_json

# def login_page(request):
#     response = render(request, "login_page.html")
#     return response

# figure out how to handle incorrect or timed out logins from API authentication
# request.method == 'POST' for when using Django-OAuth 2.0
# def home_page(request):
def view_page(request):
	if request.method == 'GET':
		response = render(request, "login_new.html")
		request_p = request.build_absolute_uri()
		splitted = request_p.split('code=')
		print()
		print("------------splitted: ", splitted)
		print(len(splitted))
		if len(splitted) > 1:
			# request_p = request.build_absolute_uri()
			# splitted = request_p.split('code=')
			# print()
			# print("------------splitted: ", splitted)
			print(API_DOCTOR)
			print(API_PATIENTS)
			code = splitted[1]
			response = requests.post('https://drchrono.com/o/token/', data={
					'code': code,
					'grant_type': 'authorization_code',
					'redirect_uri': REDIRECT_URI,
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
			json_res = make_request(API_DOCTOR, access_token) # --!
			print(json_res)
			doctor, new_doc_obj = DoctorInformation.objects.update_or_create(
				doctor_id=json_res['results'][0]['id'],
				doctor_first_name=json_res['results'][0]['first_name'],
				doctor_last_name=json_res['results'][0]['last_name'],
				doctor_data_json=json_res['results'][0]
				)
			doctor.save()
			print("DOCTOR INFO: ", doctor)
			
			json_res = make_request(API_PATIENTS, access_token) # --!
			for i in range(len(json_res['results'])):
				print('PATIENT ', i)
				for key, value in json_res['results'][i].items():
					print(key, ":", value)
				patient, new_pat_obj = PatientInformation.objects.update_or_create(
					patient_data_json=i,
				)
			response = render(request, "Home_jan18.html", {"user":doctor}, {"patient":patient})
			# response = render(request, "DC_Main_Page.html")
	else:
		response = render(request, "login_fail.html")
	
	print(response)
	return response
