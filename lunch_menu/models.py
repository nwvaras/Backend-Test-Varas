import datetime
import uuid

from django.db import models


# Create your models here.
class CreateMixin(models.Model):
    """
    Provides a mixin for annotating a DB object with timestamp and
    user information of creation.
    """

    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    modified_at = models.DateTimeField("Fecha de modificación", auto_now=True)

    class Meta:
        abstract = True


class Menu(CreateMixin):
    """
    Model referencing to the Menu of the day, for the Cornershop company.

    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # pylint: disable=invalid-name
    name = models.CharField(max_length=256)
    ready = models.BooleanField(default=False)
    day = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

    def can_choose_meal(self):
        return True if self.day == self.day else False


class Choice(models.Model):
    """
    Model referencing to the Choices availables to select for the Menu.

    """

    description = models.TextField()
    menu = models.ForeignKey(Menu, related_name="choices", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.description


class EmployeeChoice(models.Model):
    """
    Model referencing to the Employee Choice for the Menu.

    """

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    choice = models.ForeignKey(
        Choice, related_name="employee_choices", null=True, on_delete=models.CASCADE
    )
    customization = models.TextField(default="")

    def __str__(self):
        return f"{self.first_name} {self.choice}"
