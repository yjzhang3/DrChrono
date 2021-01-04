from django.urls import path
from drchrono_webapp.views import home_page

app_name = 'drchrono'
urlpatterns = [
    path('', home_page, name="home")
    # path('', index),
    # path('', views.index, name='index'),
]