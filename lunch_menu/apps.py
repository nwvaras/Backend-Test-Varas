from django.apps import AppConfig
from django.conf import settings

from lunch_menu.utils import SlackClient


class LaunchMenuConfig(AppConfig):
    name = 'lunch_menu'
    slack_client = SlackClient(settings.SLACK_TOKEN)
