from django.urls import path
from drchrono_webapp.views import login_page, home_page

# '' - first page
# 'home' - home page

app_name = 'drchrono'
urlpatterns = [
    path(r'^$', login_page, name="login"),
    path(r'^$', home_page, name="home"),
    # path('', include('django.contrib.auth.urls')),
]