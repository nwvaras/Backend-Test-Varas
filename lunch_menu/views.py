from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import permissions

from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from lunch_menu.serializers import MenuSerializer, ChoiceSerializer, EmployeeMenuChoiceSerializer
from .apps import SlackClient
from .models import Menu, Choice, Employee, EmployeeMenuChoice


class MenuViewSet(ViewSet):
    """
    Employee View Set. Contains method to obtain the menu choices for the employee
    :return If it is on time, returns a HTML template or a JSON, depending on the request. Else a 404
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated]
    template_name = 'employee_choices.html'

    def retrieve(self, request, pk=None):
        employees_choices = EmployeeMenuChoice.objects.filter(choice__menu=pk)
        return Response({'employees_choices': employees_choices, "menu_pk": pk})


# class EmployeeViewSet(ViewSet):
#     """
#     Employee View Set. Contains method to obtain the menu choices for the employee
#     :return If it is on time, returns a HTML template or a JSON, depending on the request. Else a 404
#     """
#     renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
#     template_name = 'menu_choice.html'
#
#     @action(detail=True, methods=['get'])
#     def menu_list(self, request, pk=None):
#         employee_choice = get_object_or_404(EmployeeMenuChoice, pk=pk)
#         if employee_choice.can_choose_meal():
#             serializer = EmployeeMenuChoiceSerializer(employee_choice)
#             if request.accepted_renderer.format == 'html':
#                 return Response({'serializer': serializer,
#                                  'employee_choice': employee_choice})
#             else:
#                 return Response(serializer.data)
#         else:
#             return Response(status=404)
#
#     @action(detail=True, methods=['post'])
#     def select(self, request, pk=None):
#         employee_choice = get_object_or_404(EmployeeMenuChoice, pk=pk)
#         serializer = EmployeeMenuChoiceSerializer(employee_choice, data={'choice': request.data['choice']})
#         if serializer.is_valid():
#             serializer.save()
#             if request.accepted_renderer.format == 'html':
#                 return Response({'serializer': serializer,
#                                  'employee_choice': employee_choice})
#             else:
#                 return Response(serializer.data)
#         else:
#             return Response(status=404)


class MenuCreationView(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    template_name = 'menu.html'

    def get(self, request):
        return Response({'menu_serializer': self.get_serializer_class(), "choice_serializer": ChoiceSerializer()})

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"menu_serializer": self.get_serializer_class(), "choice_serializer": ChoiceSerializer()})


class ChoiceView(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    template_name = 'choices.html'

    def get(self, request):
        return Response({"choice_serializer": ChoiceSerializer()})

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"choice_serializer": ChoiceSerializer()})


class EmployeeViewSet(ViewSet):
    """
    Employee View Set. Contains method to obtain the menu choices for the employee
    :return If it is on time, returns a HTML template or a JSON, depending on the request. Else a 404
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'menu_choice.html'

    @action(detail=True, methods=['get'])
    def menu_list(self, request, pk=None):
        employee_choice = get_object_or_404(EmployeeMenuChoice, pk=pk)
        if employee_choice.can_choose_meal():
            serializer = EmployeeMenuChoiceSerializer(employee_choice)
            if request.accepted_renderer.format == 'html':
                return Response({'serializer': serializer,
                                 'employee_choice': employee_choice})
            else:
                return Response(serializer.data)
        else:
            return Response(status=404)

    @action(detail=True, methods=['post'])
    def select(self, request, pk=None):
        employee_choice = get_object_or_404(EmployeeMenuChoice, pk=pk)
        serializer = EmployeeMenuChoiceSerializer(employee_choice, data={'choice': request.data['choice']})
        if serializer.is_valid():
            serializer.save()
            if request.accepted_renderer.format == 'html':
                return Response({'serializer': serializer,
                                 'employee_choice': employee_choice})
            else:
                return Response(serializer.data)
        else:
            return Response(status=404)
