"""AuflixTemp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include,re_path
from accounts.views import Accounts

urlpatterns = [
    re_path(r'^$',Accounts.index,name='index'),
    re_path(r'^login/',Accounts.login,name='login'),
    re_path(r'^dashboard/',Accounts.dashboard,name='dashboard'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^logout/', Accounts.logout, name='logout'),
    re_path(r'^reset_password/', Accounts.reset_password, name='reset_password'),
]
