def test_emit(discord_webhook_handler, log_record, mock_webhook, mocker, discord_fmt):
    mock_webhook.return_value = mocker.Mock()
    discord_webhook_handler.get_webhook = mock_webhook
    discord_webhook_handler.formatter = discord_fmt
    mock_instance = mock_webhook.return_value

    discord_webhook_handler.emit(log_record)

    mock_webhook.assert_called_once()
    mock_instance.add_embed.assert_called_once()
    mock_instance.execute.assert_called_once()
