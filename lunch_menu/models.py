from django.db import models
import datetime


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
    name = models.CharField(max_length=256)
    ready = models.BooleanField(default=False)
    day = models.DateField(default=datetime.date.today)
    expiration_time = models.TimeField(default=datetime.time(11, 00))
    choices = models.ManyToManyField('Choice')

    def __str__(self):
        return self.name


class Choice(models.Model):
    """
    Model referencing to the Choices availables to select for the Menu.

    """
    description = models.TextField()

    def __str__(self):
        return self.description
