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


class FilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        menu = self.context.get('menu', None)
        if menu is not None:
            return menu.choices.all()
        else:
            return EmptyQuerySet()


class EmployeeMenuChoiceSerializer(serializers.ModelSerializer):
    choice = FilteredPrimaryKeyRelatedField(allow_null=True, required=True)

    class Meta:
        model = EmployeeMenuChoice
        fields = ('menu', 'employee', 'choice')
        read_only_fields = ('menu', 'employee')
