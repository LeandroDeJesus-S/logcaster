import pytest

from django.conf import settings
from pydantic import ValidationError

from logcaster.settings._models import Environment


def test_env_with_only_telegram():
    env = Environment(telegram={'chat_id': -123444, 'bot_token': 'fake token'}, discord=None)
    stts = env.get_telegram_settings()

    assert stts.bot_token == 'fake token'
    assert stts.chat_id == -123444
    assert env.discord is None

    
def test_env_with_only_discord():
    env = Environment(discord={'webhook_url': 'https://example.com/ws'}, telegram=None)
    stts = env.get_discord_settings()

    assert stts.webhook_url == 'https://example.com/ws'
    assert env.telegram is None


def test_env_without_telegram_and_discord_but_dj():
    settings.LOGCASTER_TELEGRAM_BOT_TOKEN='fake token'
    settings.LOGCASTER_TELEGRAM_CHAT_ID=389342
    
    env = Environment(discord=None, telegram=None)
    stts = env.get_telegram_settings()

    assert stts.bot_token == 'fake token'
    assert stts.chat_id == 389342

    delattr(settings, 'LOGCASTER_TELEGRAM_BOT_TOKEN')
    delattr(settings, 'LOGCASTER_TELEGRAM_CHAT_ID')
    

def test_env_raises_exception_without_dj_discord_and_telegram(clear_env):
    with pytest.raises(ValidationError, match="A Logcaster source must be configured") as e:
        Environment(discord=None, telegram=None)