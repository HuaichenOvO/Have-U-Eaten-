from django.urls import path
from . import views
urlpatterns=[
  path('',views.index,name='index'),
  path('bill/',views.bill,name='bill'),
  path('show/',views.show,name='show'),
  path('check/',views.check,name='check'),
]