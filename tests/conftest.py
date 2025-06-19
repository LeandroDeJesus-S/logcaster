import logging

import pytest
from django.conf import settings

from logcaster.discord import DiscordFormatter, DiscordHandler
from logcaster.settings import _models
from logcaster.telegram import TelegramAsyncHandler
from logcaster.discord_utils.abstraction import AbsDiscordEmbed, AbsDiscordWebhookClient


@pytest.fixture
def log_record() -> logging.LogRecord:
    """return a log record object instance with the args bellow

    Args:
        name (str): rec name
        level (int): logging.DEBUG
        pathname (str): path/name
        lineno (int): 20
        msg (str): some message
        args (_ArgsType): None
        exc_info (_SysExcInfoType): None
    """
    return logging.LogRecord(
        name="rec name",
        level=logging.DEBUG,
        pathname="path/name",
        lineno=20,
        msg="some message",
        args=None,
        exc_info=None,
    )


@pytest.fixture
def mock_webhook(mocker):
    return mocker.MagicMock(spec=AbsDiscordWebhookClient)


@pytest.fixture
def mock_embed(mocker):
    return mocker.MagicMock(spec=AbsDiscordEmbed)


@pytest.fixture
def mock_telegram_env(mocker):
    mocker.patch.object(
        _models.Environment,
        "get_telegram_settings",
        return_value=_models.TelegramEnvironmentVars(
            bot_token="bot_token", chat_id=123
        ),
    )


@pytest.fixture
def mock_discord_env(mocker):
    mocker.patch.object(
        _models.Environment,
        "get_discord_settings",
        return_value=_models.DiscordEnvironmentVars(webhook_url="webhook_url"),
    )

@pytest.fixture
def mock_dj_env(mocker):
    mocked_settings = mocker.Mock(
        LOGCASTER_DISCORD_WEBHOOK_URL='https://discord.com',
        LOGCASTER_TELEGRAM_BOT_TOKEN='token',
        LOGCASTER_TELEGRAM_CHAT_ID=123,
    )
    mocker.patch.object(
        _models.Environment,
        "get_django_settings",
        return_value=mocked_settings,
    )

@pytest.fixture
def clear_env(monkeypatch):
    monkeypatch.delenv('DISCORD__WEBHOOK_URL', raising=False)
    monkeypatch.delenv('TELEGRAM__BOT_TOKEN', raising=False)
    monkeypatch.delenv('TELEGRAM__CHAT_ID', raising=False)

@pytest.fixture
def discord_webhook_handler():
    return DiscordHandler()


@pytest.fixture
def discord_fmt():
    return DiscordFormatter()


@pytest.fixture
def handler():
    return TelegramAsyncHandler()


def pytest_configure():
    settings.configure()
