import pytest
from logcaster.settings._environment import Environment
from django.conf import settings
from pydantic import ValidationError


def test_env_with_only_telegram():
    Environment(telegram={'chat_id': -123444, 'bot_token': 'fake token'}, discord=None)
    
def test_env_with_only_discord():
    Environment(discord={'webhook_url': 'https://example.com/ws'}, telegram=None)


def test_env_without_telegram_and_discord_but_dj():
    settings.LOGCASTER_TELEGRAM_BOT_TOKEN='fake token'
    settings.LOGCASTER_TELEGRAM_CHAT_ID=389342
    
    Environment(discord=None, telegram=None)

    delattr(settings, 'LOGCASTER_TELEGRAM_BOT_TOKEN')
    delattr(settings, 'LOGCASTER_TELEGRAM_CHAT_ID')
    

def test_env_raises_exception_without_dj_discord_and_telegram():
    expected_error_msg = 'A Logcaster source must be configured'
    with pytest.raises(ValidationError) as e:
        Environment(telegram=None, discord=None)
    
    assert e.match(expected_error_msg)
