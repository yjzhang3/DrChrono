from django.shortcuts import render
from django.http import HttpResponse
# from django.views.generic.base import TemplateView

# Create your views here.

def home_page(request):
    response = render(request, "home.html")
    return response

# class HomePage(TemplateView):
#     template_name = "index.html"

# def index(request):
#     return render(request, template_name='templates/index.html')