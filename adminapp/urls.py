"""onlinesales_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView, ListView, DeleteView
from adminapp.models import MerchantModel

from adminapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='adminapplication/index.html')),
    path('loginadmin/', views.logincheck, name='loginadmin'),
    path('home/', TemplateView.as_view(template_name='adminapplication/welcome.html'), name='home'),
    path('logout/', TemplateView.as_view(template_name='adminapplication/index.html'), name='logout'),
    path('addmerchant/', views.addmerchant),
    path('savemerchant/', views.savemerchant, name='savemerchant'),
    path('viewmerchant/', ListView.as_view(model=MerchantModel, template_name='adminapplication/viewmerchant.html', context_object_name='merchant')),
    path('editmerchant/', ListView.as_view(model=MerchantModel, template_name='adminapplication/editmerchant.html'), name='editmerchant'),
    path('deleteMerchant<int:pk>/', DeleteView.as_view(model=MerchantModel, success_url='/adminapp/editmerchant/', template_name='adminapplication/deletemerchant.html'), name='deleteMerchant'),

    path('checkuser/<str:username>/<str:password>/', views.Checkuser.as_view()),
    path('resetpassword/<str:email>/', views.Changepassword.as_view()),
    path('changepassword/<str:email>/<str:password>/', views.Changeoldpassword.as_view()),

    path('saveproduct/', views.Saveproduct.as_view()),
    path('viewproduct/<str:idno>/', views.ViewProduct.as_view()),
    path('deleteproduct/<str:idno>/', views.DeleteProduct.as_view()),

    path('updaterequest/<str:id>/', views.UpdateRequest.as_view()),
    path('saveupdate/<str:id_no>/', views.SaveUpdate.as_view())
]
