from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymysql import NULL
from .decorators import unauthenticated_user
from .models import *
from .views import *
from .forms import *

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
import random


# Create your views here.


#------------------------ user stuffs ------------------------
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            # print(request.POST.get('username'))
            uname = request.POST.get('username')[0],
            email = request.POST.get('email')[0],
            # print("Created: ", email)
            pwd_1 = request.POST.get('password1')[0],
            token = str(random.random()).split('.')[1]
            t = Token(uname=uname, email=email, pwd_1=pwd_1, token=token)
            t.save()

            # 网页跳转、发送验证短信
            myDomain = get_current_site(request).domain
            link = f'http://{myDomain}/verify/{token}'

            send_mail(
                'CSC4001 Verification',
                f'Successful registration! Please click the following link to finish the email\
verification: {link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return HttpResponse("The message has been sent!")

    context = {'form':form}
    return render(request, 'real_nets/register.html', context)

@unauthenticated_user
def verify(request, token):
    try:
        token = Token.objects.get(token=token)
        print(token.uname, token.email)
    except Exception as ex:
        messages.error(request, "Validation failed.")
        return redirect("Register")

    # 注册及激活完成之后的内容
    if request.method == "POST":
        try:

            user = User(username = token.uname,
                email = token.email,
                password = token.pwd_1,
            )
            user.save()
        except Exception as ex:
            return HttpResponse(ex)

        try:
            new_client = Client(
                user = user,
                phone = NULL
            )
            new_client.save()

            group = Group.objects.get(name='Customer')
            user.groups.add(group)

            username = token.uname
            messages.success(request, 'Account was created for ' + username)

            return redirect('Login')
        
        except Exception as ex:
            return HttpResponse(ex)

    context = {}
    return render(request, 'real_nets/valid_success.html', context)


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
def profile_update(request):
    request_client = request.user.client
    form = ClientUpdateForm(instance=request_client)
    #调用form中的注册表并渲染进url指定的html文件中
    if request.method == "POST":
        # print("On Click1")
        # 根据 <input name=Submit value=xxx>的value值来确定是哪一个input按钮
        if request.POST["Submit"] == "confirm": 
            # print("On Click2")
            form = ClientUpdateForm(request.POST, request.FILES, instance=request_client)
            if form.is_valid():
                print("Confirmed and valid!")
                form.save()
                return redirect(profile)

    context = {"form": form}
    return render(request, 'real_nets/profile_update.html', context)

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