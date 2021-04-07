from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from lunch_menu.serializers import LoginSerializer, MenuSerializer, ChoiceSerializer, EmployeeMenuChoiceSerializer
from .apps import SlackClient
from .models import Menu, Choice, Employee, EmployeeMenuChoice


class MenuCreationView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu.html'

    def get(self, request):
        return Response({'menu_serializer': MenuSerializer(), "choice_serializer": ChoiceSerializer()})


class ChoiceView(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = ChoiceSerializer
    template_name = 'choices.html'

    def get(self, request):
        return Response({"choice_serializer": ChoiceSerializer()})

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"choice_serializer": ChoiceSerializer()})


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        return Response({'serializer': LoginSerializer()})


class EmployeeViewSet(ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu_choice.html'

    @action(detail=True, methods=['get'])
    def menu_list(self, request, pk=None):
        employee_choice = EmployeeMenuChoice.objects.get(pk=pk)
        menu = employee_choice.menu
        return Response(
            {'employee_choice_serializer': EmployeeMenuChoiceSerializer(employee_choice, context={"menu": menu}),
             "menu": menu,'employee_choice': employee_choice})

    @action(detail=True, methods=['post'])
    def select(self, request, pk=None):
        employee_choice = EmployeeMenuChoice.objects.get(pk=pk)
        menu = employee_choice.menu
        employee_serializer = EmployeeMenuChoiceSerializer(employee_choice,data={'choice': request.data['choice']},context={"menu":menu})
        employee_serializer.is_valid()
        employee_serializer.save()
        return Response(
            {'employee_choice_serializer': EmployeeMenuChoiceSerializer(employee_choice, context={"menu": menu}),
             "menu": menu,'employee_choice': employee_choice})
