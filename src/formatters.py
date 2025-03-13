import logging


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


__all__ = ['DiscordFormatter']