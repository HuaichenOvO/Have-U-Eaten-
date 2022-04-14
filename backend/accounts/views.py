from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

# 存放 functions


def home(request):
    clients = Client.objects.all()
    addrs = Address.objects.all()
    context = {"addrs" : addrs, "clients": clients}
    return render(request, 'accounts/home.html', context)

def contact(request):
    return render(request, 'accounts/contact.html')

def customer(request):
    clients = Client.objects.all()

    # {"objs": Objs}中， "objs"是目标html里使用的变量，Objs是数据库传到html的变量
    return render(request, 'accounts/customer.html', {'clients':clients})

def products(request):
    return render(request, 'accounts/products.html')
