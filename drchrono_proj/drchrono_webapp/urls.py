from django.urls import path
from drchrono_webapp.views import login_page, home_page

app_name = 'drchrono'
urlpatterns = [
    path('login', login_page, name="login"),
    path('home', home_page, name="home"),
    # path('', include('django.contrib.auth.urls')),
]