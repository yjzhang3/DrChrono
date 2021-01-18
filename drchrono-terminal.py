import requests, json, datetime, pytz, subprocess, sys, urllib3
urllib3.disable_warnings()

def main_app(access_token, refresh_token):
    doc_url = 'https://app.drchrono.com/api/doctors'
    json_res = make_request(doc_url, access_token)
    doc_id = json_res['results'][0]['id']
    doc_firstname = json_res['results'][0]['first_name']
    doc_lastname = json_res['results'][0]['last_name']

    while 1:
        print('---------------\nHello, Dr. ' + doc_lastname + '!\n')
        print('1. Print all patients (lengthy!)\n2. Print doctor information\n3. Search for a patient\n4. Look up patient information using patient ID\n5. TODO Send a quick message using patient ID\n\n0. Exit\n\n')
        option = input('DrDash Terminal > ')

        if option=='0':
            break
        elif option=='1':
            test_api_url = 'https://app.drchrono.com/api/patients'
            json_res = make_request(test_api_url, access_token)
            for i in range(len(json_res['results'])):
                for key, value in json_res['results'][i].items():
                    print(key, ":", value)
        elif option=='2':
            test_api_url = 'https://app.drchrono.com/api/doctors'
            json_res = make_request(test_api_url, access_token)
            for i in range(len(json_res['results'])):
                print('\n')
                for key, value in json_res['results'][i].items():
                    print(key, ":", value)
        elif option=='3':
            searchstring = input("Enter the search string: ")
            test_api_url = 'https://app.drchrono.com/api/patients'
            json_res = make_request(test_api_url, access_token)
            searchres = search(json_res, searchstring)
            length = len(searchres)
            if length < 1:
                print("No results")
            else:
                print("Found " + str(length) + " result(s)")
                for i in range(length):
                    print(searchres[i])
        elif option=='4':
            patient_id = input("Please enter patient ID: ")
            if len(str(patient_id)) > 8 or str(patient_id).isdigit() != 1:
                print("This is not a valid patient ID!")
            else:
                url = "https://app.drchrono.com/api/patients/" + str(patient_id)
                json_file = make_request(url, access_token)
                print("Patient info being shown for patient ID " + str(patient_id))
                print("First name: " + json_file['first_name'])
                print("Last name: " + json_file['last_name'])
                print("Gender: " + json_file['gender'])
                print("Cell phone: " + json_file['cell_phone'])
                print("Full address: " + json_file['address'] + ", " + json_file['city'] + ", " + json_file['state'])
                print("Pharmacy ID: " + json_file['default_pharmacy'])

        # print(api_call_response.text)
        
def make_request(url, access_token):
    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_call_response = requests.get(url, headers=api_call_headers, verify=False)
    api_json = api_call_response.json()
    return api_json

def search(json_file, searchstring):
    searchres = []
    tekr = 0
    for i in range(len(json_file['results'])):
        for key, value in json_file['results'][i].items():
            if key=='first_name' or key=='last_name':
                newval = value.lower()
                if searchstring.lower()==newval.lower():
                    searchres.insert(tekr, json_file['results'][i]['first_name'] + " " + json_file['results'][i]['last_name'] + "," + str(json_file['results'][i]['id']))
                    tekr = tekr + 1
    return searchres

print("DrDash 1.01")
print("----------")
answer = input("Are you logged in? (yes/debug/exit): ")

if answer=='yes':
    access_token = input('access_token: ')
    refresh_token = input('refresh token: ')
    main_app(access_token, refresh_token)
elif answer=='no':
    code = input('code: ')
    response = requests.post('https://drchrono.com/o/token/', data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://drdash.herokuapp.com/',
        'client_id': 'gCVCP45fvAZqwlQvB6d4CUqEFlonrXTCjbr90BLm',
        'client_secret': 'ZvfvYGFNkabOPiLhQYlxacUWS8c1mA6Sc8Ec0XEaPhaYBCXMy1l89qyXDqMA8XbAQCHmnfuEf6BchB9WGBaeTTkpRe4B7Y9HlJVbAIR1NLVmkpwXQ3b0Vh3ax1LIQM3R',
    })
    response.raise_for_status()
    data = response.json()

    # Save these in your database associated with the user
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])
elif answer=='debug':
    main_app('CCdp8mvLYMWNaVWRodrgx95BtaAkt6', 'ETQUgVbs6SmYWu6p2u82y9nF0vw3hX')
elif answer=='exit':
    print('exiting...')
else:
    print(answer + ' : command not recognized')
