# EasyLog
A package to send loggings to discord, telegram and whatever other location with the proposal of easily implements observability to small and lower coast applications

<p align="center">🛠🔧 Project in development process 🔧🛠</p>

### Available sources
- Discord
- Telegram

### Features
- [x] easy to use.
- [x] natively supported by the built-in python logging package.
- [ ] async support.


### Quick-start
Requirements
- [python](https://pyton.org) >=3.10,<4.0
- [poetry](https://python-poetry.org)

#### Install
```sh
# by defaults supports telegram setup
poetry add easylog

# discord
poetry add "easylog[discord]"
```

#### Configure
Once installed, you need only set the environment vars (see: [.env example file]('.env-example'))
```yml
# .env
TELEGRAM__BOT_TOKEN=<you bot token>
TELEGRAM__CHAT_ID=<the chat id which the bot will send logs>
```

#### Usage
```py
import logging
from easylog.telegram import TelegramHandler, TelegramFormatter

logger = logger.getLogger('my-application-logger')

handler = TelegramHandler()
formatter = TelegramFormatter(include_fields=['message', 'asctime'])

handler.setFormatter(formatter)
logger.addLogger(logger)
```

**Note**: The default level is setting up to ERROR, it's highly recommended don't set a lower level, cause each emitted logging will make a request to the given source.


#### Django example
```py
# settings.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "telegram_fmt": {
            "class": "easylog.telegram.TelegramFormatter",
        },
        "discord_fmt": {
            "class": "easylog.discord.DiscordFormatter",
            "exclude_fields": ['funcName', 'lineno'],
        }
    },
    "handlers": {
        "telegram": {
            "class": "easylog.telegram.TelegramHandler",
        },
        "discord": {
            "class": "easylog.discord.DiscordHandler",
            "exclude_fields": ['funcName', 'lineno'],
        }
    },
    "loggers": {
        "easy": {
            "handlers": ["telegram", "discord"],
            "formatters": ["telegram_fmt", "discord_fmt"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
```