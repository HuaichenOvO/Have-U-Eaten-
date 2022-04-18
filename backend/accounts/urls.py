"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# the url.py in APP
from django.contrib import admin
from django.urls import path, include
from accounts import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.profile, name= "Home"),

    # user stuffs
    path('register/', views.registerPage, name="Register"),
	path('login/', views.loginPage, name="Login"),  
	path('logout/', views.logoutUser, name="Logout"),
	path('verify/<str:token>', views.verify),
	# path('valid_success/', views.logoutUser, name="Logout"),
	# path('valid_failure/', views.logoutUser, name="Logout"),

    # real net part:
    path('profile/', views.profile, name= "Profile"),
    path('profile_update/', views.profile_update, name= "Profile_update"),

    path('tasks/', views.tasks, name= "Tasks"),
    path('tasks_create/<str:pk>', views.tasks_create, name= "Tasks_create"),
    
    path('delivery/', views.delivery, name= "Delivery"),
    
    path('order/', views.order, name= "Order"),
    
    path('address/', views.address, name= "Address"),
    path('address_create/<str:pk>', views.address_create, name= "Address_create"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
