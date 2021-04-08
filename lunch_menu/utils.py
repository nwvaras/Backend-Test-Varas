from django.conf import settings

from slack_sdk import WebClient


class SlackClient:
    def __init__(self, token):
        self.client = WebClient(token=token)
