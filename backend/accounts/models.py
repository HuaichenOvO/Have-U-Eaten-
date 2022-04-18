from django.db import models
from django.contrib.auth.models import User


"""
1. 用户| Client     | 用户名 密码 邮箱 手机号 头像img 加入日期 完成订单数 coins# 
2. 订单| Order      | 收方ID、送方ID、订单ID、外卖地址、送达地址、预计时间、悬赏金额、外卖信息img
3. 任务| Post       | 收方ID、外卖地址、送达地址、预计时间、悬赏金额、外卖信息img
4. 地址| Address    | 区域(某书院/teaching/others) 楼(ABCD/新图/。。。) 楼房号
5. 信息| Message    | 发送者、收悉者、时间戳、内容
6. 通知| Notice     | 收信者、标题、内容、已读
"""


class Token(models.Model):
    uname = models.CharField(max_length=100)
    email = models.EmailField()
    pwd_1 = models.CharField(max_length=100)
    token = models.CharField(max_length=100)


class Client(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=100, blank=True, default="Anonymous"+str(id))
    phone = models.CharField(max_length=200, null=True)
    coin_num = models.IntegerField(default=2)
    tasks_delivered = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_created=True, auto_now_add=True, null=True)
    photo = models.ImageField(null=True, blank=True, default="ohh.png")
    # models, forms, views, html, settings
    # orders = models.ManyToManyField(Order) # 如果一个用户对应的多个xx，可以使用manytomanyField

    def __str__(self):
        return self.nick_name

class Address(models.Model):
    AREA = (
        ('Harmonia','Harmonia'),
        ('Shaw','Shaw'),
        ('Muse','Muse'),
        ('Diligentia','Diligentia'),
        ('Startup','Startup'),
        ('Teaching','Teaching'),
        ('Others','Others'),
    )
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    area = models.CharField(max_length=200, null=True, choices=AREA) #choices相当于一个枚举
    building = models.CharField(max_length=50, null=True)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.area + " " + self.building + str(self.number)

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'), 
        ('Sending','Sending'),
        ('Claiming','Claiming'),# arrived
        ('Canceled','Canceled'),
        ('Done','Done'),
    )
    buyer = models.ForeignKey(User, related_name="as_buyer", null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(User, related_name="as_sender", null=True, on_delete=models.SET_NULL)
    coin_reward = models.IntegerField(null=True)
    take_addr = models.ForeignKey(Address, related_name="as_start_addr",  null=True,on_delete=models.SET_NULL)
    send_addr = models.ForeignKey(Address, related_name="as_target_addr", null=True, on_delete=models.SET_NULL)
    exp_min = models.IntegerField(default=30)
    note = models.TextField(max_length=4000, blank=True, default="None")
    status = models.CharField(max_length=200, default='Pending', choices=STATUS)
    food_info = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.buyer.client.nick_name + "'s order- " + str(self.id)

    def can_cancel(self) -> bool:
        if (self.status == "Pending"): return  True
        else: return False

    def is_picked(self) -> bool:
        if (self.status == "Sending" or self.status=="Claiming"): return  True
        else: return False

    def is_arrived(self) -> bool:
        if (self.status=="Claiming"): return  True
        else: return False


class Task(models.Model):
    buyer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    coin_reward = models.IntegerField(null=True)
    take_addr = models.ForeignKey(Address, related_name="tobe_start_addr",  null=True,on_delete=models.SET_NULL)
    send_addr = models.ForeignKey(Address, related_name="tobe_target_addr", null=True, on_delete=models.SET_NULL)
    exp_min = models.IntegerField(default=30)
    note = models.TextField(max_length=4000, null=True, blank=True, default="None")
    food_info = models.ImageField(null=True, blank=True)
    post_time = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.buyer.client.nick_name + "'s post- " + str(self.id)

# class Message(models.Model):
#     sender = models.ForeignKey(User, related_name="as_mes_sender", on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, related_name="as_mes_receiver", on_delete=models.CASCADE)
#     mes_time = models.DateTimeField(auto_created=True, auto_now_add=True)
#     mes_content = models.TextField(max_length=4000, null=False)

# class Foo(models.Model):
#     cli = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL, related_name="gods")
#     point = models.IntegerField(null=True)
# # 获取指向某个client的所有foo： 1. clients=Client.objects.all();  for cli in clients: foos = cli.gods.all()
# # 2. 1. client1=Client.objects.get(id=10086); foos = client1.gods.all()