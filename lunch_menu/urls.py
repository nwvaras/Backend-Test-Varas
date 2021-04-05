from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from lunch_menu.views import MenuView



# Private End-points

urlpatterns = [url(r'^$', MenuView.as_view(), name='menu'),]


