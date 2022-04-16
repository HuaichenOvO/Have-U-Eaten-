from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import unauthenticated_user
from .models import *
from .views import *
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages


# Create your views here.

# 存放 functions

@login_required(login_url='Login')
def home(request):
    clients = Client.objects.all()
    addrs = Address.objects.all()
    context = {"addrs" : addrs, "clients": clients}
    return render(request, 'accounts/home.html', context)

def contact(request):
    return render(request, 'accounts/contact.html')

def customer(request, pk_test):
    client = Client.objects.get(id = pk_test)



    # {"objs": Objs}中， "objs"是目标html里使用的变量，Objs是数据库传到html的变量
    return render(request, 'accounts/customer.html', {'client':client})

def products(request):
    return render(request, 'accounts/products.html')


#------------------------ user stuffs ------------------------
@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='Customer')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return redirect('Login')
		

	context = {'form':form}
	return render(request, 'real_nets/register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect("Profile")
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'real_nets/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('Login')

#------------------------ Real Net Parts ------------------------
@login_required(login_url='Login')
def profile(request):
    return render(request, 'real_nets/profile.html')

@login_required(login_url='Login')
def tasks(request):
    if request.method == "POST":
        pk = request.POST["Submit"]
        # print("Clicked delete: ", pk)
        task = Task.objects.get(id=pk)
        task.delete()

    tasks = Task.objects.all()
    num = tasks.count()
    context = {"tasks": tasks, "task_num": num}
    return render(request, 'real_nets/tasks.html', context)

@login_required(login_url='Login')
def tasks_create(request, pk=0):
    #调用form中的注册表并渲染进url指定的html文件中
    if pk==0 :
        form = TaskCreateForm() 
        # create
    else:
        task = Task.objects.filter(id=pk).first()
        form = TaskCreateForm(instance=task) 
        # update  # filter().first()防止报错

    if request.method == "POST":
        # 根据 <input name=Submit value=xxx>的value值来确定是哪一个input按钮
        if request.POST["Submit"] == "confirm": 
            if pk==0: 
                form = TaskCreateForm(request.POST)
            else: 
                form = TaskCreateForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect(tasks)

    context = {"form": form}
    return render(request, 'real_nets/tasks_create.html', context)

@login_required(login_url='Login')
def delivery(request):
    
    context = {}    
    return render(request, 'real_nets/delivery.html', context)

# 测试是否可行！
@login_required(login_url='Login')
def order(request):
    # take order
    if request.method == "POST":
        pk = request.POST["Submit"]
        task = Task.objects.get(id=pk)
        k = 1            # ！！需要获取登录用户的信息！！
        new_order = Order(
            buyer = task.buyer,
            sender = Client.objects.get(id=k),
            coin_reward = task.coin_reward,
            take_addr = task.take_addr,
            send_addr = task.send_addr,
            exp_min = task.exp_min,
            note = task.note,
            status = task.status,
            food_info = task.food_info
        )
        new_order.save()
    
    context = {}    
    return render(request, 'real_nets/order.html', context)

@login_required(login_url='Login')
def notice(request):
    
    context = {}    
    return render(request, 'real_nets/notice.html', context)

@login_required(login_url='Login')
def message(request):
    
    context = {}    
    return render(request, 'real_nets/message.html', context)

@login_required(login_url='Login')
def address(request):
    users = Client.objects.all()
    addrs = []
    for user in users:
        addr = user.address_set.all()
        for adr in addr:
            addrs.append(adr)

    context = {"address": addrs}
    return render(request, 'real_nets/address.html', context)

@login_required(login_url='Login')
def address_create(request):
    #调用form中的注册表并渲染进url指定的html文件中
    form = AddressCreateForm() 
    if request.method == "POST":
        # 根据 <input name=Submit value=xxx>的value值来确定是哪一个input按钮
        if request.POST["Submit"] == "create_address": 
            form = AddressCreateForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(address)

    context = {"form": form}
    return render(request, 'real_nets/address_create.html', context)