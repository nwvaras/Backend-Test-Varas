from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from lunch_menu.views import MenuViewSet, delete_choice

# Private End-points
router = DefaultRouter()
# router.register(r'employee', EmployeeViewSet, 'choice')
router.register(r"menu", MenuViewSet, "menu")

urlpatterns = [
    path(r"choice/<int:pk>/delete/", delete_choice, name="choice-delete"),
] + router.urls
