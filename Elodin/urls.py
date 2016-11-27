"""Elodin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.generic import TemplateView

from NamesDatabase.views import index, delete, login_user, logout_user, signup_user, logs

urlpatterns = [
    url(r'^$', index),
    url(r'^logs$', logs),
    url(r'^delete/(?P<pk>[0-9]+)$', delete),
    url(r'^admin/', admin.site.urls),
    url(r'^login$', login_user),
    url(r'^logout$', logout_user),
    url(r'^signup$', signup_user),
    url(r'^conducta$', TemplateView.as_view(template_name='conducta.html'))

]
