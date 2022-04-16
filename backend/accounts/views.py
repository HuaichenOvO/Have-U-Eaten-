from django.http import HttpResponse
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from .models import *
from .views import *
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from pymysql import NULL


# Create your views here.

# 存放 functions

@login_required(login_url='Login')
def home(request):
    clients = Client.objects.all()
    addrs = Address.objects.all()
    context = {"addrs" : addrs, "clients": clients}
    return render(request, 'accounts/home.html', context)


#------------------------ user stuffs ------------------------
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            new_client = Client(
                user = user,
                phone = NULL
            )
            new_client.save()
        
            group = Group.objects.get(name='Customer')
            user.groups.add(group)

            username = form.cleaned_data.get('username')
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
    user = request.user
    context = {"usr": user}
    return render(request, 'real_nets/profile.html', context)

@login_required(login_url='Login')
def tasks(request):
    if request.method == "POST":
        cmd_value = request.POST["Submit"]
        cmd_name = (cmd_value.split('@'))[0]
        cmd_id = (cmd_value.split('@'))[1]

        if cmd_name == "Delete":
            task = Task.objects.filter(id=cmd_id).first()
            task.delete()

        elif cmd_name == "Claim":
            task = Task.objects.filter(id=cmd_id).first()
            username = request.user.username
            new_order = Order(
                buyer = task.buyer,
                sender = User.objects.get(username = username),
                coin_reward = task.coin_reward,
                take_addr = task.take_addr,
                send_addr = task.send_addr,
                exp_min = task.exp_min,
                note = task.note,
                food_info = task.food_info
            )
            new_order.save()
            task.delete()
            print("order created")

    other_tasks = Task.objects.exclude(buyer=request.user)
    my_tasks = Task.objects.filter(buyer=request.user)
    num = other_tasks.count()
    context = {"other_tasks": other_tasks, 
        "my_tasks": my_tasks, 
        "task_num": num}
    return render(request, 'real_nets/tasks.html', context)

@login_required(login_url='Login')
def tasks_create(request, pk=0):
    #调用form中的注册表并渲染进url指定的html文件中
    if pk==0 :
        form = TaskCreateForm(initial=
            {"take_addr" : "e.g. NorthGate",
            "send_addr" : "e.g. TeachingA-999",}
        ) 
        # create
    else:
        task = Task.objects.filter(id=pk).first()
        form = TaskCreateForm(instance=task) 
        # update  # filter().first()防止报错

    if request.method == "POST":
        if request.POST["Submit"] == "confirm": 
            if pk==0: 
                form = TaskCreateForm(request.POST)
            else: 
                form = TaskCreateForm(request.POST, instance=task)
            if form.is_valid():
                form.instance.buyer = request.user
                form.save()
                return redirect(tasks)

    context = {"form": form}
    return render(request, 'real_nets/tasks_create.html', context)

@login_required(login_url='Login')
def delivery(request):
    deliveries = Order.objects.filter(sender=request.user.id)

    # deliveries = Order.objects.filter(buyer.id==request.user.id)

    context = {"deliveries": deliveries}    
    return render(request, 'real_nets/delivery.html', context)

@login_required(login_url='Login')
def order(request):
    orders = Order.objects.filter(buyer=request.user.id)

    # orders = Order.objects.all()
    
    context = {"orders": orders}    
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
    addrs = Address.objects.filter(owner=request.user.id)
    context = {}
    if addrs.count()>0:
        context["address"] = addrs
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
                form.instance.owner = request.user
                form.save()
                return redirect(address)

    context = {"form": form}
    return render(request, 'real_nets/address_create.html', context)