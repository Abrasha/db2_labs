from django.conf.urls.static import static

from djangomongo import settings
from djangomongo import views

"""djangomongo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

urlpatterns = [
                  url(r'^$', views.index, name='admin'),
                  url(r'^admin/', admin.site.urls, name='admin'),
                  url(r'^messages/$', views.messages, name='messages'),
                  url(r'^users/$', views.get_users, name='users'),
                  url(r'^delete_message/$', views.delete_messages, name='delete_messages')
              ] + static(settings.STATIC_URL)
