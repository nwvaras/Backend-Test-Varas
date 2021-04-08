from celery import shared_task

from lunch_menu.models import Menu
from .apps import LaunchMenuConfig


from .serializers import ChoiceSerializer


@shared_task
def send_reminders(menu_id):
    """Celery task to send menu to employees."""
    slack = LaunchMenuConfig.slack_client
    employees = slack.users_list()["members"]
    menu = Menu.objects.prefetch_related("choices").get(pk=menu_id)
    for employee in employees:
        print(employee)
        if not employee["is_bot"] and employee["id"] != "USLACKBOT":
            options = ChoiceSerializer(menu.choices.all(), many=True).data
            slack.reminder(employee, menu.get_menu_url(), menu.name, options)
