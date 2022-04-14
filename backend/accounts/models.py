import email
from django.db import models

# Create your models here.

# app 里需要注意的核心文件
# 用来初始化数据库

"""
1. 订单 | 收方ID、送方ID、订单ID、外卖地址、送达地址、预计时间、悬赏金额、外卖信息img
2. 用户 | 用户名 密码 邮箱 手机号 头像img 加入日期 完成订单数 coins# 
3. 任务 | 收方ID、外卖地址、送达地址、预计时间、悬赏金额、外卖信息img
4. 地址 | 区域(某书院/teaching/others) 楼(ABCD/新图/。。。) 楼房号
"""

class Client(models.Model):
    name = models.CharField(max_length=200, null=True)
    pwd = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    coin_num = models.IntegerField(default=0)
    tasks_delivered = models.IntegerField(default=0)
    # orders = models.ManyToManyField(Order) # 如果一个用户对应的多个xx，可以使用manytomanyField

    def __str__(self):
        return self.name

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

    area = models.CharField(max_length=200, null=True, choices=AREA) #choices相当于一个枚举
    building = models.CharField(max_length=50, null=True)
    number = models.IntegerField(null=True)

    def __str__(self):
        return self.area + " " + self.building + str(self.number)

class Order(models.Model):
    buyer = models.ForeignKey(Client, related_name="as_buyer", null=True, on_delete=models.SET_NULL)
    sender = models.ForeignKey(Client, related_name="as_sender", null=True, on_delete=models.SET_NULL)
    take_addr = models.ForeignKey(Address, related_name="take_food_from",  null=True,on_delete=models.SET_NULL)
    send_addr = models.ForeignKey(Address, related_name="send_food_to", null=True, on_delete=models.SET_NULL)
    exp_time = models.DateTimeField(auto_now_add=True, null=True)
    coin_reward = models.IntegerField(null=True)
    food_info = models.ImageField(null=True)

    def __str__(self):
        return self.sender.name + " take for " + self.buyer.name + "-" + str(self.pk)

# class Foo(models.Model):
#     cli = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL, related_name="gods")
#     point = models.IntegerField(null=True)
# # 获取指向某个client的所有foo： 1. clients=Client.objects.all();  for cli in clients: foos = cli.gods.all()
# # 2. 1. client1=Client.objects.get(id=10086); foos = client1.gods.all()