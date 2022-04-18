from ast import Return
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib import messages
from pymysql import NULL
import random
from .decorators import unauthenticated_user
from .models import *
from .views import *
from .forms import *


# Create your views here.


#------------------------ user stuffs ------------------------
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            uname = form.cleaned_data.get('username'),
            email = form.cleaned_data.get('email')
            pwd_1 = form.cleaned_data.get('password1'),

            if not (User.objects.filter(username=uname).exists()):
                token = str(random.random()).split('.')[1]
                t = Token(uname=uname, email=email, pwd_1=pwd_1, token=token)
                t.save()

                # 网页跳转、发送验证短信
                myDomain = get_current_site(request).domain
                link = f'http://{myDomain}/verify/{token}'

                try:
                    send_mail(
                        'CSC4001 Verification',
                        f'Successful registration! Please click the following link to finish the email verification: {link}',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    return HttpResponse("The message has been sent!")
                except Exception as ex:
                    context = {"title":"Invalid Registration", "msg": ex}
                    return render(request, 'real_nets/info.html', context)
            else: 
                context = {"title":"Invalid Registration", "msg":"User already exists."}
                return render(request, 'real_nets/info.html', context)

    context = {'form':form}
    return render(request, 'real_nets/register.html', context)

@unauthenticated_user
def verify(request, token):
    try:
        myToken = Token.objects.get(token=token)
    except Exception as ex:
        messages.error(request, "Validation failed.")
        return redirect("Register")

    # 注册及激活完成之后的内容
    if request.method == "POST":
        try:
            uname = myToken.uname[2:-3]
            pwd = myToken.pwd_1[2:-3]
            user = User(username = uname,
                email = myToken.email,
                password = pwd,
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

            group = Group.objects.get(name='Client')
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
    try:
        request_client = request.user.client
        form = ClientUpdateForm(instance=request_client)
    except Exception:
        form = ClientUpdateForm()
    #调用form中的注册表并渲染进url指定的html文件中
    if request.method == "POST":
        # print("On Click1")
        # 根据 <input name=Submit value=xxx>的value值来确定是哪一个input按钮
        if request.POST["Submit"] == "confirm": 
            # print("On Click2")
            try:    
                form = ClientUpdateForm(request.POST, request.FILES, instance=request_client)
            except:
                form = ClientUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                print("Confirmed and valid!")
                form.save()
                return redirect(profile)

    context = {"form": form}
    return render(request, 'real_nets/profile_update.html', context)

@login_required(login_url='Login')
def tasks(request):
    other_tasks = Task.objects.exclude(buyer=request.user)
    my_tasks = Task.objects.filter(buyer=request.user)
    num = other_tasks.count()
    context = {"other_tasks": other_tasks, 
        "my_tasks": my_tasks, 
        "task_num": num}

    if request.method == "POST":
        cmd_value = request.POST["Submit"]
        cmd_name = (cmd_value.split('@'))[0]
        cmd_id = (cmd_value.split('@'))[1]

        if cmd_name == "Delete":
            print(request.POST)
            task = Task.objects.filter(id=cmd_id).first()
            try:
                fee = task.coin_reward
            except Exception as ex:
                messages.success(request, ex)
                render(request, 'real_nets/tasks.html', context)
            task = Task.objects.filter(id=cmd_id).first()
            cli = Client.objects.get(user = request.user.id)
            cli.coin_num += fee
            cli.save()
            task.delete()
            messages.success(request, 'Deleted')
            render(request, 'real_nets/tasks.html', context)

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
            messages.success(request, 'Cliamd')
            return render(request, 'real_nets/tasks.html', context)

    return render(request, 'real_nets/tasks.html', context)

@login_required(login_url='Login')
def tasks_create(request, pk):
    context = {}
    # render the form into HTML
    if int(pk)==0 :
        # create
        form = TaskCreateForm(initial=
            {"take_addr" : "e.g. NorthGate",
            "send_addr" : "e.g. TeachingA-999",}
        ) 
        context.update({"form": form, "update": ""})
    else:
        # update  
        # filter().first()防止报错
        task = Task.objects.filter(id=pk).first()
        form = TaskCreateForm(instance=task) 
        context.update({"form": form, "update": "true"})

    if request.method == "POST":
        if request.POST["Submit"] == "confirm": 
            if int(pk)==0: 
                fee = int(request.POST["coin_reward"])
                cash = request.user.client.coin_num
                if (fee < 0):
                    messages.error(request, 'Positive coin number required')
                    render(request, 'real_nets/tasks_create.html', context)
                elif (fee <= cash):
                    form = TaskCreateForm(request.POST, request.FILES)
                    cli = Client.objects.get(user = request.user.id)
                    cli.coin_num -= fee
                    cli.save()
                    request.user.client.coin_num -= fee
                else:
                    messages.error(request, 'No enough coins')
                    render(request, 'real_nets/tasks_create.html', context)
            else: 
                form = TaskCreateForm(request.POST, request.FILES, instance=task)
            if form.is_valid():
                form.instance.buyer = request.user
                form.save()
                return redirect(tasks)

    context = {"form": form}
    return render(request, 'real_nets/tasks_create.html', context)

@login_required(login_url='Login')
def delivery(request):
    # deliveries = Order.objects.filter(buyer.id==request.user.id)
    deliveries1 = Order.objects.filter(Q(sender=request.user.id) & Q(status="Pending") | Q(status="Sending") | Q(status="Claiming"))
    deliveries2 = Order.objects.filter(Q(sender=request.user.id) & Q(status="Canceled") | Q(status="Done"))
    context = {"delivery1": deliveries1, "delivery2": deliveries2}    

    if request.method == "POST":
        cmd_value = request.POST["Submit"]
        cmd_name = (cmd_value.split('@'))[0]
        cmd_id = (cmd_value.split('@'))[1]

        if cmd_name == "got":
            order = Order.objects.filter(id=cmd_id).first()
            order.status=("Sending")
            order.save()
            messages.success(request, 'Picked')
            render(request, 'real_nets/delivery.html', context)             
        elif cmd_name == "done":
            order = Order.objects.filter(id=cmd_id).first()
            order.status=("Claiming")
            order.save()
            messages.success(request, 'Claimed arrival')
            render(request, 'real_nets/delivery.html', context)             

    return render(request, 'real_nets/delivery.html', context)

@login_required(login_url='Login')
def order(request):
    orders1 = Order.objects.filter(Q(buyer=request.user.id) & Q(status="Pending") | Q(status="Sending") | Q(status="Claiming"))
    orders2 = Order.objects.filter(Q(buyer=request.user.id) & Q(status="Canceled") | Q(status="Done"))
    context = {"order1": orders1, "order2": orders2}    
    
    if request.method == "POST":
        try:
            cmd_value = request.POST["Submit"]
            cmd_name = (cmd_value.split('@'))[0]
            cmd_id = (cmd_value.split('@'))[1]

            if cmd_name == "Cancel":
                order = Order.objects.filter(id=cmd_id).first()
                print("cancel")
                order.status=("Canceled")
                order.save()
                messages.success(request, 'Canceled')
                render(request, 'real_nets/order.html', context)                
            elif cmd_name == "Received":
                order = Order.objects.filter(id=cmd_id).first()
                print("done")
                order.status=("Done")
                order.save()
                sender = order.sender.client
                fee = order.coin_reward
                sender.coin_num += fee
                sender.save()
                messages.success(request, 'Received')
                render(request, 'real_nets/order.html', context)
        except Exception as ex:
            pass

    return render(request, 'real_nets/order.html', context)

@login_required(login_url='Login')
def address(request):
    addrs = Address.objects.filter(owner=request.user.id)
    context = {"address": addrs}
    # if addrs.count()>0:
    #     context["address"] = addrs
    if request.method == "POST":
        try:
            cmd_value = request.POST["Submit"]
            cmd_name = (cmd_value.split('@'))[0]
            cmd_id = (cmd_value.split('@'))[1]

            print(cmd_value, cmd_name, cmd_id)

            if cmd_name == "Delete":
                addr = Address.objects.filter(id=cmd_id).first()
                addr.delete()
                messages.success(request, 'Deleted')
                render(request, 'real_nets/address.html', context) 

        except Exception as ex:
            messages.success(request, ex)
            render(request, 'real_nets/address.html', context) 
    return render(request, 'real_nets/address.html', context)

@login_required(login_url='Login')
def address_create(request, pk):
    #调用form中的注册表并渲染进url指定的html文件中
    if int(pk)==0 :
        form = AddressCreateForm() 
        # create
    else:
        addr = Address.objects.filter(id=int(pk)).first()
        form = AddressCreateForm(instance=addr) 
        # print (form)
        # update  # filter().first()防止报错
    
    #调用form中的注册表并渲染进url指定的html文件中
    form = AddressCreateForm() 
    if request.method == "POST":
        if request.POST["Submit"] == "create_address": 
            if int(pk)==0: 
                form = AddressCreateForm(request.POST)
            else: 
                form = AddressCreateForm(request.POST, instance=addr)
            if form.is_valid():
                form.instance.owner = request.user
                form.save()
                return redirect(address)

    context = {"form": form}
    return render(request, 'real_nets/address_create.html', context)