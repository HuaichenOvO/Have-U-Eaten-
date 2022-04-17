from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import *
import re

# class RegistrationForm(ModelForm):
#     class Meta:
#         model = RegistrationTmpModel
#         fields = ["uname", "email", "pword1", "pword2"]


#     def is_valid(self) -> bool:
#         password = self.Meta.model.pword1

#         flag = False
#         while True:
#             if password!=self.Meta.model.pword2:
#                 flag = False
#                 break
#             elif (len(password)<8):
#                 flag = False
#                 break
#             elif not re.search("[a-z]", password):
#                 flag = False
#                 break
#             elif not re.search("[A-Z]", password):
#                 flag = False
#                 break
#             elif not re.search("[0-9]", password):
#                 flag = False
#                 break
#             elif not re.search("[_@$]", password):
#                 flag = False
#                 break
#             elif re.search("\s", password):
#                 flag = False
#                 break
#             else:
#                 flag = True
#                 break
#         return flag


class ClientUpdateForm(ModelForm):
    class Meta:
        model = Client
        fields = ["nick_name", "phone", "photo"]


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task # 声明注册到哪一个数据库中
        fields = ['coin_reward', 'take_addr', 'send_addr', 'exp_min', 'note', 'food_info']

class AddressCreateForm(ModelForm):
    class Meta:
        model = Address
        exclude = ["owner"]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
