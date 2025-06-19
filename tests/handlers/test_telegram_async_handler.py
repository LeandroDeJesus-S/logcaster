from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from logcaster.exceptions import EmitError
from logcaster.telegram import TelegramAsyncHandler


@pytest.mark.asyncio
async def test_emit_success(capsys, mock_telegram_env):
    handler = TelegramAsyncHandler()
    record = MagicMock()
    record.format.return_value = "log message"
    
    mock_post = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    mock_client_instance = MagicMock()
    mock_client_instance.post = mock_post
    mock_client_instance.__aenter__.return_value = mock_client_instance
    mock_client_instance.__aexit__.return_value = None

    with patch("httpx.AsyncClient", return_value=mock_client_instance):
        await handler._emit(record)

    mock_post.assert_called_once()
    captured = capsys.readouterr()
    assert "Logging sent to telegram chat id" in captured.out


@pytest.mark.asyncio
async def test_emit_http_error(mock_telegram_env):
    handler = TelegramAsyncHandler()
    record = MagicMock()
    record.format.return_value = "log message"

    
    mock_response = MagicMock()
    mock_response.status_code = 400

    expected_exception = httpx.HTTPError('error')
    expected_exception.request = MagicMock()
    mock_response.raise_for_status.side_effect = expected_exception

    mock_post = AsyncMock()
    mock_post.return_value = mock_response

    mock_client_instance = MagicMock()
    mock_client_instance.post = mock_post
    mock_client_instance.__aenter__.return_value = mock_client_instance
    mock_client_instance.__aexit__.return_value = None

    with patch("httpx.AsyncClient", return_value=mock_client_instance) as mock_client:
        with pytest.raises(EmitError) as e:
            await handler._emit(record)

    mock_client.return_value.post.assert_called_once()
    assert e.match(r"error when logging to telegram: .+ - .+")
