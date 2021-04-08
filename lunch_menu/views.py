from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .apps import SlackClient
from .models import Choice, EmployeeChoice, Menu
from .serializers import (
    ChoiceSerializer,
    CreateChoiceSerializer,
    EmployeeChoiceSerializer,
    MenuSerializer,
)
from rest_framework.decorators import api_view


class MenuViewSet(ViewSet, CreateAPIView):
    ##TODO: Edit menu, add buttons to add choices in edit view, slack celery, refactor fixtures in test, fix what happens when there is no pk in obtain
    """
    Menu View Set. Contains method to obtain the menu choices for the employee
    :return If it is on time, returns a HTML template or a JSON, depending on the request. Else a 404
    """

    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get_serializer_class(self):
        if self.action == "get_add_choices_form":
            return ChoiceSerializer
        elif self.action == "add_choices":
            return CreateChoiceSerializer
        elif self.action == "retrieve" or self.action == "choices":
            return EmployeeChoiceSerializer
        else:
            return MenuSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Only retrieve is free for everyone. Every other action requires authentication
        """
        if self.action == "retrieve":
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        """
        POST /menu/
        Create a new menu from the request.
        """
        super().create(request)
        return Response(
            {
                "menu_serializer": self.get_serializer_class(),
                "choice_serializer": ChoiceSerializer(),
            },
            template_name="menu.html",
        )

    @action(detail=False, methods=["get"], name="Create menu for the day")
    def add(self, request):
        """
        GET /menu/add/
        Obtain menu creator template.
        """
        return Response(
            {
                "menu_serializer": self.get_serializer_class(),
                "choice_serializer": ChoiceSerializer(),
            },
            template_name="menu.html",
        )

    @action(detail=True, methods=["post"], name="Create employee menu choice")
    def employee_choice(self, request, pk=None):
        """
        POST /menu/:pk/employee_choice/
        Obtain employee choice creator template.
        """
        menu = Menu.objects.get(pk=pk)
        employee_choice_serializer = EmployeeChoiceSerializer(
            data=request.data, context={"menu": menu}
        )
        if employee_choice_serializer.is_valid():
            employee_choice_serializer.save()
            if request.accepted_renderer.format == "html":
                return Response(
                    {"serializer": employee_choice_serializer, "menu": menu},
                    template_name="menu_choice.html",
                )
            else:
                return Response(employee_choice_serializer.data)
        else:
            return Response(status=404)

    def retrieve(self, request, pk=None):
        """
        GET /menu/:pk/ method
        Obtain menu form to choice lunch meal.
        """
        menu = Menu.objects.prefetch_related("choices").get(pk=pk)
        employee_choice_serializer = self.get_serializer_class()(context={"menu": menu})
        if menu.can_choose_meal():
            if request.accepted_renderer.format == "html":
                return Response(
                    {"menu": menu, "serializer": employee_choice_serializer},
                    template_name="menu_choice.html",
                )
            else:
                return Response(employee_choice_serializer.data)
        else:
            return Response(status=404)

    @action(detail=True, methods=["get"], name="Get all employee choices for the menu")
    def choices(self, request, pk=None):
        """
        GET /menu/:pk/choices/
        Obtain all employee choices for the menu.
        """
        choices = Choice.objects.filter(menu_id=pk)
        employees_choices = EmployeeChoice.objects.filter(choice__in=choices)
        return Response(
            {
                "serializer": self.get_serializer_class(),
                "employees_choices": employees_choices,
            },
            template_name="employee_choices.html",
        )

    @action(detail=True, methods=["post"], name="Create choices for the menu")
    def add_choices(self, request, pk=None):
        """
        POST /menu/:pk/add_choices/
        Create choice for menu.
        """

        serializer = self.get_serializer_class()(
            data={"description": request.data["description"], "menu": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return redirect("menu:menu-change", pk=pk)
        else:
            return redirect("menu:menu-add-choices", pk=pk)

    @add_choices.mapping.get
    def get_add_choices_form(self, request, pk=None):
        """
        GET /menu/:pk/add_choices/
        Obtain view to add choices to the menu.
        """
        return Response(
            {"serializer": self.get_serializer_class(), "menu_pk": pk},
            template_name="choices.html",
        )

    @action(detail=True, methods=["post"], name="Change menu information")
    def change(self, request, pk=None):
        """
        POST /menu/:pk/add_choices/
        Update menu information.
        """

        serializer = self.get_serializer_class()(
            data={"description": request.data["description"], "menu": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return redirect("menu:menu-change", pk=pk)
        else:
            return redirect("menu:menu-add-choices", pk=pk)

    @change.mapping.get
    def get_change_form(self, request, pk=None):
        """
        GET /menu/:pk/add_choices/
        Obtain view to edit menu.
        """
        menu = Menu.objects.get(pk=pk)
        return Response(
            {"serializer": self.get_serializer_class()(menu), "menu": menu},
            template_name="menu_edit.html",
        )

    @action(detail=True, methods=["post"], name="Change menu information")
    def get_change_form(self, request, pk=None):
        """
        GET /menu/:pk/add_choices/
        Obtain view to edit menu.
        """
        menu = Menu.objects.get(pk=pk)
        return Response(
            {"serializer": self.get_serializer_class()(menu), "menu": menu},
            template_name="menu_edit.html",
        )


@api_view(["POST"])
def delete_choice(request, pk=None):
    Choice.objects.filter(pk=pk).delete()
    return redirect("menu:menu-change", pk=request.data["menu_pk"])
