"""yihang_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from yihang_website.admin_site import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'', include('job.urls', namespace='job')),
    url(r'', include('company.urls', namespace='company')),
    # url(r'', include('accounts.urls', namespace='accounts')),
    # url(r'', include('job.urls', namespace='job')),
]
