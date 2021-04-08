import datetime

from django.db.models.query import EmptyQuerySet
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from lunch_menu.models import Choice, EmployeeChoice, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("name", "day")

    def create(self, validated_data):
        menu = Menu.objects.create(**validated_data)
        return menu


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("description",)


class CreateChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("description", "menu")


class FilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        menu = self.context.get("menu", None)
        if menu is not None:
            return menu.choices.all()
        else:
            return EmptyQuerySet()


class EmployeeChoiceSerializer(serializers.ModelSerializer):
    choice = FilteredPrimaryKeyRelatedField(allow_null=True, required=True)

    class Meta:
        model = EmployeeChoice
        fields = ("first_name", "last_name", "choice", "customization")
