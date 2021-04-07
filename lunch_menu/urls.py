from django.conf.urls import url
from django.urls import path

from rest_framework.routers import DefaultRouter

from lunch_menu.views import MenuCreationView, LoginView, ChoiceView, EmployeeViewSet, MenuViewSet

# Private End-points
router = DefaultRouter()
router.register(r'employee', EmployeeViewSet, 'choice')
router.register(r'view', MenuViewSet, 'view')

# urlpatterns = [url(r'^account/$',account_list,name='menu-choice')]
urlpatterns = [url(r'^$', MenuCreationView.as_view(), name='menu_creation'),url(r'choices/$', ChoiceView.as_view(), name='choices'),
               url('login/$', LoginView.as_view(), name='login')]

urlpatterns += router.urls
