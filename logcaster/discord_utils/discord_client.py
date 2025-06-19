from re import match

import httpx

from .abstraction import AbsDiscordEmbed, AbsDiscordWebhookClient
from .models import WebhookClientPayload


class DiscordWebhookClient(AbsDiscordWebhookClient):
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url
        if not match(
            r'^https?://discord.com/api/webhooks/[0-9]+/[a-zA-Z0-9]+$',
            self.webhook_url,
        ):
            raise ValueError(
                f'Invalid webhook url: {self.webhook_url}. '
                'Expected format: https://discord.com/api/webhooks/[id]/[token]'
        )
        self._payload: WebhookClientPayload | None = None

    def add_embed(self, embed: AbsDiscordEmbed) -> None:
        if not isinstance(embed, AbsDiscordEmbed):
            raise ValueError(
                f'Invalid embed type: {type(embed)}. '
                'Expected type: AbsDiscordEmbed'
            )

        if self._payload is None:
            self._payload = WebhookClientPayload(embeds=[embed.embed])
            return

        if self._payload.embeds is None:
            self._payload.embeds = [embed.embed]
            return

        self._payload.embeds.append(embed.embed)

    @property
    def content(self) -> str | None:
        if self._payload is None:
            return None
        return self._payload.content

    @content.setter
    def content(self, value: str) -> None:
        self._payload = WebhookClientPayload(content=value)

    def execute(self) -> None:
        if self._payload is None:
            raise ValueError('No payload to send')

        response = httpx.post(
            self.webhook_url,
            json=self._payload.model_dump(),
        )

        response.raise_for_status()

        self._payload = None
