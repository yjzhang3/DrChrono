from django.shortcuts import render
from django.http import HttpResponse
# from authlib.django.client import OAuth

# USE .ENV FILE FOR API TOKENS AND KEYS
# CLIENT_ID = 'RmxLsz3PqHVeEPBTtGw61cMVBYe8B0lLmKM7pHfV'
# CLIENT_SECRET = '9ynHMLp9e7ZG45bkQyNbItlYLTwfyrkB2MXeaPOCMmt0W55Q73qezR7H9b2JZDrvlqFNs4FqeIE38OYnXbCmOhOc4Xn44kcpvsFcqGBsGdel9NNka6bxVs8GnGwqavu6'
# oauth = OAuth()

# oauth.register(
#     name='DrChrono',
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     redirect_uri='http://127.0.0.1:8000/drchrono_webapp/home_page/callback' # replace this with postman
#     access_token_url='https://github.com/login/oauth/access_token',
#     authorize_url='https://github.com/login/oauth/authorize',
#     api_base_url='https://api.github.com/',
#     client_kwargs={'scope': 'user:email'},
# )

def login_page(request):
    response = render(request, "login_page.html")
    return response

# figure out how to handle incorrect or timed out logins from API authentication
# request.method == 'POST' for when using OAuth 2.0
def home_page(request):
    if request.method == 'GET':
        response = render(request, "login_success.html")
    else:
        response = render(request, "login_fail.html")
    return response