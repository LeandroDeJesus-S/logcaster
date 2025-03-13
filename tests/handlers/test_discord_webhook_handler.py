import logging
import pytest
from src.handlers import DiscordWebhookHandler
from src.settings import ENV

handler = DiscordWebhookHandler()


@pytest.mark.parametrize('level,expected_color', [
    (logging.DEBUG, "3498db"),
    (logging.INFO, "2ecc71"),
    (logging.WARNING, "f1c40f"),
    (logging.ERROR, "e74c3c"),
    (logging.CRITICAL, "8e44ad"),
])
def test_get_color(log_record, level, expected_color):
    """test if _get_color return the correct color to the level"""
    log_record.levelno = level
    result = handler._get_color(log_record)
    assert result == expected_color


def test_get_embed_fields_passing_only_fields(log_record):
    """test if get_embed_fields return the correct fields when passing
    the fields argument
    """
    handler = DiscordWebhookHandler(fields=('levelname', 'lineno'))
    expected_result = {'levelname': log_record.levelname, 'lineno': log_record.lineno}
    fields = handler._get_embed_fields(log_record)
    assert fields == expected_result


def test_get_embed_fields_passing_only_exclude(log_record):
    """test if get_embed_fields return the correct fields when passing
    the exclude argument
    """
    handler = DiscordWebhookHandler(exclude=('levelname', 'lineno', 'exc_info'))
    expected_result = {k: v for k,v in log_record.__dict__.items() if k not in handler.exclude}
    fields = handler._get_embed_fields(log_record)
    assert fields == expected_result


def test_pass_both_fields_and_exclude_raises_assertion_error():
    """test if raises assertion error when fields and exclude are given together"""
    with pytest.raises(AssertionError):
        DiscordWebhookHandler(fields=('lineno',), exclude=('message',))


def test_emit_creates_webhook_if_none(discord_webhook_handler, log_record, mock_webhook, mock_embed, mocker):
    discord_webhook_handler.get_webhook = mocker.MagicMock(return_value=None)  # Simula ausência de webhook
    discord_webhook_handler.get_embed = mocker.MagicMock(return_value=None)  # Simula ausência de embed
    mock_instance = mock_webhook.return_value

    discord_webhook_handler.emit(log_record)

    mock_webhook.assert_called_once_with(
        ENV.discord.webhook_url, allow_mentions={"users": "Low"}
    )
    mock_instance.add_embed.assert_called_once()
    mock_instance.execute.assert_called_once()



def test_emit_uses_existing_webhook(mocker, discord_webhook_handler, log_record, mock_webhook, mock_embed):
    mock_webhook_instance = mock_webhook.return_value
    discord_webhook_handler.get_webhook = mocker.MagicMock(return_value=mock_webhook_instance)
    discord_webhook_handler.get_embed = mocker.MagicMock(return_value=None)

    discord_webhook_handler.emit(log_record)

    mock_webhook.assert_not_called()  # Não deve criar um novo webhook
    mock_webhook_instance.add_embed.assert_called_once()
    mock_webhook_instance.execute.assert_called_once()


def test_emit_creates_embed_if_none(mocker, discord_webhook_handler, log_record, mock_webhook, mock_embed):
    mock_webhook_instance = mock_webhook.return_value
    discord_webhook_handler.get_webhook = mocker.MagicMock(return_value=mock_webhook_instance)
    discord_webhook_handler.get_embed = mocker.MagicMock(return_value=None)
    mock_embed_instance = mock_embed.return_value

    discord_webhook_handler.emit(log_record)

    mock_embed.assert_called_once_with(
        title=log_record.levelname,
        description=log_record.getMessage(),
        color=discord_webhook_handler._get_color(log_record),
    )
    mock_embed_instance.set_author.assert_called_once_with(name=discord_webhook_handler.author)
    mock_embed_instance.set_footer.assert_called_once_with(text="powered by @Low")
    mock_embed_instance.set_timestamp.assert_called_once()
    mock_webhook_instance.add_embed.assert_called_once_with(mock_embed_instance)
    mock_webhook_instance.execute.assert_called_once()