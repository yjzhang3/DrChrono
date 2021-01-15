from django.urls import path
# from drchrono_webapp.views import login_page, home_page
from drchrono_webapp.views import view_page
from django.views.generic.base import TemplateView

# '' - first page
# 'home' - home page

app_name = 'drchrono'
urlpatterns = [
    path('', view_page),
]