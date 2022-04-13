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

    def __str__(self):
        return self.name

class Order(models.Model):
    ID_buyer = models.CharField(max_length=200, null=True)
    ID_sender = models.CharField(max_length=200, null=True)
    take_addr = models.CharField(max_length=200, null=True)
    send_addr = models.CharField(max_length=200, null=True)
    exp_time = models.DateTimeField(auto_now_add=True, null=True)
    coin_reward = models.IntegerField(max_length=200, null=True)
    food_info = models.ImageField(null=True)

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

    area = models.CharField(max_length=200, null=True, choices=AREA)
    building = models.CharField(max_length=50, null=True)
    number = models.IntegerField(max_length=200, null=True)
