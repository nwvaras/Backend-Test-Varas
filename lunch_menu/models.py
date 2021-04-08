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

    EXPIRE_TIME = datetime.time(23, 00)
    SEND_TIME = datetime.datetime.now().time()

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # pylint: disable=invalid-name
    name = models.CharField(max_length=256)
    ready = models.BooleanField(default=False)
    day = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name

    def can_choose_meal(self):
        return (
            datetime.datetime.combine(self.day, self.EXPIRE_TIME)
            < datetime.datetime.now()
        )

    def get_menu_url(self):
        return f"http://localhost:8000/menu/{self.pk}/"


class Choice(models.Model):
    """
    Model referencing to the Choices availables to select for the Menu.

    """

    description = models.TextField()
    menu = models.ForeignKey(Menu, related_name="choices", on_delete=models.CASCADE)

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
