"""lostflag URL Configuration

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
from django.urls import re_path, path
from lostflag.views import index, flag, countryFlag, report

urlpatterns = [
    path('', index, name="home"),
    path('country/<cName>', countryFlag, name="countryFlag"),
    path('report', report, name='reportedRoute'),
    re_path('flag', flag, name="pctfFlag")
]