from django.urls import path
from . import views
urlpatterns=[
  path('',views.index,name='index'),
  path('dingdan/',views.dingdan,name='dingdan'),
  path('show/',views.show,name='show'),
  path('check/',views.check,name='check'),
]