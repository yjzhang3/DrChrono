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
        print('1. Print all patients (lengthy!)\n2. Print doctor information\n3. Search for a patient\n\n0. Exit\n\n')
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
            searchres = -1
            searchsurname = input("Enter the surname of your patient: ")
            test_api_url = 'https://app.drchrono.com/api/patients'
            json_res = make_request(test_api_url, access_token)
            for i in range(len(json_res['results'])):
                for key, value in json_res['results'][i].items():
                    if searchsurname==value and key=='last_name':
                        searchres = i
            if searchres==-1:
                print("No results")
            else:
                print(json_res['results'][searchres].items())
        else:
            print('unrecognized command')

        # print(api_call_response.text)

def make_request(url, access_token):
    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_call_response = requests.get(url, headers=api_call_headers, verify=False)
    api_json = api_call_response.json()
    return api_json

print("DrDash 1.01")
print("----------")
answer = input("Are you logged in? (yes/debug/exit): ")

if answer=='yes':
    access_token = input('access_token: ')
    refresh_token = input('refresh token: ')
    expires_timestamp = input('expires_timestamp: ')
    main_app(access_token, refresh_token)
elif answer=='no':
    code = input('code: ')
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
elif answer=='debug':
    main_app('Kuy5dQbqo9jSh5SFoirdZFXBx3rpOF', 'rBer32rOY1bfrLEiCoIx0XGOVL1MIK')
elif answer=='exit':
    print('exiting...')
else:
    print(answer + ' : command not recognized')
