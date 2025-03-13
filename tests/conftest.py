import logging
import pytest
from  src.handlers import DiscordWebhookHandler


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
        name='rec name',
        level=logging.DEBUG,
        pathname='path/name',
        lineno=20,
        msg='some message',
        args=None,
        exc_info=None,
    )


@pytest.fixture
def mock_webhook(mocker):
    return mocker.patch("src.handlers.DiscordWebhook")


@pytest.fixture
def mock_embed(mocker):
    return mocker.patch("src.handlers.DiscordEmbed")


@pytest.fixture
def discord_webhook_handler():
    return DiscordWebhookHandler()
