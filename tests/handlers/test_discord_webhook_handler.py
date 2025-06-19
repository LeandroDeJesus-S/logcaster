from logcaster.discord import DiscordHandler
from logcaster.discord_utils.abstraction import AbsDiscordWebhookClient


def test_emit(log_record, mocker, discord_fmt):
    webhook_client = mocker.MagicMock(spec=AbsDiscordWebhookClient)
    webhook = mocker.MagicMock()
    webhook.return_value = webhook_client
    
    discord_wh_handler = DiscordHandler()
    discord_wh_handler.formatter = discord_fmt
    discord_wh_handler.get_webhook = webhook

    discord_wh_handler.emit(log_record)

    discord_wh_handler.get_webhook.assert_called_once()
    webhook_client.add_embed.assert_called_once()
    webhook_client.execute.assert_called_once()
