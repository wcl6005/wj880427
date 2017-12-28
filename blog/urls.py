# -*- coding: utf-8 -*-

"""djangopro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views
urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    
    url(r'^billing/(?P<page>\d*)?$', views.billing, name='billing'), #正则表达式(?P<page>\d*)?
    url(r'^customer/(?P<page>\d*)?$', views.customer, name='customer'),#正则表达式(?P<page>\d*)?
    url(r'^add/billing/$', views.addBilling, name='add_billing'),
    url(r'^add/customer/$', views.addCustomer, name='add_customer'),
    url(r'^makexlsx/$', views.makexlsx, name="makexlsx"),

]
