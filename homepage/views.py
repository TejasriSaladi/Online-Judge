from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
# Create your views here.
def home_page(request):
    template = loader.get_template('homepage.html')
    context = {}
    return HttpResponse(template.render(context,request))

def login_view(request):
    return redirect('/auth/login')

def register_view(request):
    return redirect('/auth/register')