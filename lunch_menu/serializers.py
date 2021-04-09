import datetime

from django.db.models.query import EmptyQuerySet
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from lunch_menu.models import Choice, EmployeeChoice, Menu


class MenuSerializer(serializers.ModelSerializer):
    """
    Menu Serializer to use as a form or create a menu
    """

    class Meta:
        model = Menu
        fields = ("name", "day")


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Choice Serializer to use as a form. Doesn't not contain a menu, so it's only to use as a form
    """

    class Meta:
        model = Choice
        fields = ("description",)


class CreateChoiceSerializer(serializers.ModelSerializer):
    """
    Choice Serializer only used to create Choices.
    """

    class Meta:
        model = Choice
        fields = ("description", "menu")


class FilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    """
    Field to use when we want to limit a related field by a QuerySet
    """

    def get_queryset(self):
        menu = self.context.get("menu", None)
        if menu is not None:
            return menu.choices.all()
        else:
            return EmptyQuerySet()


class EmployeeChoiceSerializer(serializers.ModelSerializer):
    """
    EmployeeChoice Serializer. Uses as a form and as a creation serializer.
    """

    choice = FilteredPrimaryKeyRelatedField(allow_null=False, required=True)

    class Meta:
        model = EmployeeChoice
        fields = ("first_name", "last_name", "choice", "customization")
