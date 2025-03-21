import json
import logging
import sys
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from discord_webhook import DiscordEmbed, DiscordWebhook

from .formatters import DiscordFormatter
from .settings import ENV


class DiscordWebhookHandler(logging.Handler):
    COLORS = {
        logging.DEBUG: "3498db",  # blue
        logging.INFO: "2ecc71",  # green
        logging.WARNING: "f1c40f",  # yellow
        logging.ERROR: "e74c3c",  # red
        logging.CRITICAL: "8e44ad",  # purple
    }
    DEFAULT_FORMATTER_KWRDS = {
        "fmt": "%(levelname)s %(asctime)s %(module)s.%(funcName)s:%(lineno)d %(message)s"
    }

    def __init__(
        self,
        author="EasyLog",
        thumbnail_url=None,
        image_url=None,
        level=logging.ERROR,
        fields: tuple[str] = None,
        exclude: tuple[str] = None,
        formatter_kwargs: dict | None = None,
    ):
        assert not (fields and exclude), "`fields` and `exclude` are exclusionary"
        assert level in self.COLORS, (
            f"the log level must one of: {list(self.COLORS.keys())}"
        )
        assert isinstance(author, str), "author must be str"
        assert isinstance(image_url, str) or image_url is None, (
            "image_url must be str or None"
        )
        assert isinstance(thumbnail_url, str) or thumbnail_url is None, (
            "thumbnail_url must be str or None"
        )
        assert isinstance(formatter_kwargs, dict) or formatter_kwargs is None, (
            "formatter_kwargs must be dict or None"
        )
        assert isinstance(fields, tuple) or fields is None, (
            "fields must be tuple or None"
        )
        assert isinstance(exclude, tuple) or exclude is None, (
            "exclude must be tuple or None"
        )

        super().__init__(level)
        self.formatter = DiscordFormatter(
            **(formatter_kwargs or self.DEFAULT_FORMATTER_KWRDS)
        )
        self.author = author
        self.thumbnail = thumbnail_url
        self.image = image_url
        self.fields = fields
        self.exclude = exclude or ("msg", "message", "levelname")

    def _get_color(self, record: logging.LogRecord) -> str:
        """return the hex color by the record.levelno attribute"""
        return self.COLORS[record.levelno]

    def get_webhook(self) -> DiscordWebhook | None:
        """hook method to get an custom DiscordWebhook object instance"""
        pass

    def get_embed(self, record: logging.LogRecord) -> DiscordEmbed | None:
        """hook method to get the DiscordEmbed instance

        Args:
            record (logging.LogRecord): receives the log record object for convenience.
        """
        pass

    def _get_embed_fields(self, record: logging.LogRecord) -> dict[str, Any]:
        """return a dictionary with the fields and values that will be sent to discord log

        Args:
            record (logging.LogRecord): the log record object

        Returns:
            dict[str, Any]: fields and values that will be sent like embed fields
        """
        if self.fields is None:
            return {f: v for f, v in record.__dict__.items() if f not in self.exclude}
        return {f: v for f, v in record.__dict__.items() if f in self.fields}

    def emit(self, record: logging.LogRecord) -> None:
        # TODO: maybe a module to emitters can be good to avoid coupling with DiscordWebhook
        # TODO: move embed to formatter
        webhook = self.get_webhook() or DiscordWebhook(
            ENV.discord.webhook_url,
            allow_mentions={"users": "Low"},
        )

        embed = self.get_embed(record) or DiscordEmbed(
            title=record.levelname,
            description=record.getMessage(),
            color=self._get_color(record),
        )

        self.thumbnail and embed.set_thumbnail(self.thumbnail)
        self.image and embed.set_image(self.image)

        embed.set_author(name=self.author)

        embed.set_footer(text="powered by @Low")
        embed.set_timestamp()

        [
            embed.add_embed_field(name=field, value=str(value))
            for field, value in self._get_embed_fields(record).items()
        ]

        webhook.add_embed(embed)
        webhook.execute()


class TelegramHandler(logging.Handler): # TODO: add tests
    def __init__(self, level = logging.ERROR):
        super().__init__(level)
        self.URL = f"https://api.telegram.org/bot{ENV.telegram.bot_token}/sendMessage"

    def emit(self, record):
        out = self.format(record)
        out = f"```\n{out}\n```"

        data = json.dumps(
            {"text": out, "chat_id": ENV.telegram.chat_id, "parse_mode": "MarkdownV2"}
        ).encode("utf-8")
        request = Request(
            self.URL, data=data, headers={"Content-Type": "application/json"}
        )

        try:
            response = urlopen(request)
            sys.stdout.write(f"{response.read().decode()}\n")

        except HTTPError as e:
            sys.stdout.write(f"error when logging to telegram: {e.read().decode()}\n")

        except Exception as e:
            sys.stdout.write(f"error when logging to telegram: {str(e)}\n")
            sys.stdout.write(out + "\n")

        return None


__all__ = ["DiscordWebhookHandler", "TelegramHandler"]
