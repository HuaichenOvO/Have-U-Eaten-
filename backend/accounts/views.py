from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# 存放 functions


def home(request):
    return render(request, 'accounts/home.html')

def contact(request):
    return render(request, 'accounts/contact.html')

def customer(request):
    return render(request, 'accounts/customer.html')

def products(request):
    return render(request, 'accounts/products.html')
