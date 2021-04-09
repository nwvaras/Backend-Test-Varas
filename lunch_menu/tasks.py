from celery import shared_task
from django.conf import settings

from lunch_menu.models import Menu

from .serializers import ChoiceSerializer
from .utils import SlackClient


@shared_task
def send_reminders(menu_id):
    """
    Celery task to send messages to employees.
    :param menu_id: A menu id/pk
    :return: Nothing
    """
    slack = SlackClient(settings.SLACK_TOKEN)
    employees = slack.users_list()["members"]
    menu = Menu.objects.prefetch_related("choices").get(pk=menu_id)
    for employee in employees:
        if not employee["is_bot"] and employee["id"] != "USLACKBOT":
            options = ChoiceSerializer(menu.choices.all(), many=True).data
            slack.message(employee, menu.get_menu_url, menu.name, options)
