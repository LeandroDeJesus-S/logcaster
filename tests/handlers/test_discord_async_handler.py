from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from logcaster.exceptions import EmitError
from logcaster.discord import DiscordAsyncHandler


@pytest.mark.asyncio
async def test_emit_success(capsys, mock_discord_env, log_record):
    handler = DiscordAsyncHandler()
    client = MagicMock()
    client_instance = MagicMock()
    client_instance.execute = AsyncMock()

    client.return_value = client_instance
    handler.get_webhook = client

    with patch("httpx.AsyncClient", return_value=client):
        await handler._emit(log_record)

    client_instance.execute.assert_called_once()
    captured = capsys.readouterr()
    assert "logger sent to discord" in captured.out


@pytest.mark.asyncio
async def test_emit_error(mock_discord_env, log_record, capsys):
    expected_exception = Exception('error')

    handler = DiscordAsyncHandler()
    client = MagicMock()
    client_instance = MagicMock()
    client_instance.execute = AsyncMock(side_effect=expected_exception)

    client.return_value = client_instance
    handler.get_webhook = client

    with patch("httpx.AsyncClient"):
        with pytest.raises(EmitError) as e:
            await handler._emit(log_record)

    assert e.match(r"fail to sending logging to Discord")
