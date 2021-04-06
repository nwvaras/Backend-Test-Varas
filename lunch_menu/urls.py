from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from lunch_menu.views import MenuView, LoginView, ChoiceView

# Private End-points

urlpatterns = [url(r'^$', MenuView.as_view(), name='menu'),url(r'choices/$', ChoiceView.as_view(), name='choices'),
               url('login/$', LoginView.as_view(), name='login')]


