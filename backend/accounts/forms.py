from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import *


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
