from datetime import datetime

from django.db.models.query import EmptyQuerySet
from rest_framework import serializers

from lunch_menu.models import Menu, Choice, EmployeeMenuChoice


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'



class EmployeeMenuChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeMenuChoice
        fields = ('employee', 'choice','customization')
        read_only_fields = ('menu', 'employee')

    def validate(self, data):
        """
        Check the time of creation.
        """
        if not self.instance.can_choose_meal():
            raise serializers.ValidationError("Menu choice must be selected before 11 AM CLT!")
        return data