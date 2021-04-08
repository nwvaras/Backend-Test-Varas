from django.conf import settings

from slack_sdk import WebClient


class SlackClient:
    def __init__(self, token):
        print(token)
        self.client = WebClient(token=token)

    def users_list(self):
        return self.client.users_list()

    def _get_block_style_from_options(self, options):
        block_options = list(
            map(
                lambda opt: {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": f"Option {opt[0] + 1} : {opt[1]['description']}",
                    },
                },
                enumerate(options),
            )
        )
        return block_options

    def reminder(self, user, link, popup_text, options):
        ending_block = {
            "type": "section",
            "text": {"type": "plain_text", "text": "Have a nice day!"},
        }
        options_block = self._get_block_style_from_options(options)
        blocks = [
            {"type": "header", "text": {"type": "plain_text", "text": "Hello!"}},
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f" I share with you today's menu {popup_text} :)",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Go to this link to choose your meal: {link}",
                },
            },
            {"type": "divider"},
        ]

        blocks += options_block
        blocks.append(ending_block)
        return self.client.chat_postMessage(
            text=popup_text, channel=user["id"], blocks=blocks
        )
