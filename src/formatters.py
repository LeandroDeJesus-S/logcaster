import logging
import texttable
from tabulate import tabulate


class DiscordFormatter(logging.Formatter):
    EMOJIS = {
        logging.DEBUG: "\U0001f41b",  # 🐛
        logging.INFO: "\U0001f4ac",  # 💬
        logging.WARNING: "\U000026a0",  # ⚠️
        logging.ERROR: "\U00002757",  # ❗
        logging.CRITICAL: "\U0001f4a5",  # 💥
    }

    RESET = "\033[0m"

    def _get_emoji(self, record):
        return self.EMOJIS.get(record.levelno, "")

    def _get_level_name(self, record):
        emoji = self._get_emoji(record)
        levelname = f"{emoji} {record.levelname} {emoji}"
        return levelname

    def format(self, record):
        record.levelname = self._get_level_name(record)
        return super().format(record)


class TelegramFormatter(logging.Formatter):
    def __init__(self, include_fields=None, exclude_fields=None):
        super().__init__()
        self.include_fields = include_fields or []
        self.exclude_fields = exclude_fields or []

    def format(self, record):
        record_dict = record.__dict__

        if self.include_fields:
            data = {key: record_dict[key] for key in self.include_fields if key in record_dict}
        else:
            data = {key: value for key, value in record_dict.items() if key not in self.exclude_fields}

        # Converter para tabela
        table = tabulate(data.items(), tablefmt='presto', headers=['field', 'value'])
        return table


__all__ = ['DiscordFormatter', 'TelegramFormatter']
