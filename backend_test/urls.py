"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import include, path

from lunch_menu.urls import urlpatterns as lunch_url

from .utils.healthz import healthz

urlpatterns = [
    path("healthz", healthz, name="healthz"),
    url("", include((lunch_url, "menu"), namespace="menu"), name="menu"),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^login/$", LoginView.as_view(template_name="login.html"), name="login"),
]
