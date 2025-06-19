import pytest
from logcaster.discord_utils.discord_client import DiscordWebhookClient, DiscordWebhookAsyncClient
from logcaster.discord_utils.discord_embed import DiscordEmbed


@pytest.mark.parametrize(
    'webhook_url,should_raise',
    [
        ('https://discord.com/api/webhooks/123/abc', False),
        ('https://discord.com/api/webhooks/123', True),
        ('https://discord.com/api/webhooks/123/abc/def', True),
    ])
def test_client_url_pattern(webhook_url, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            DiscordWebhookClient(webhook_url)
        return

    client = DiscordWebhookClient(webhook_url)
    assert client.webhook_url == webhook_url


def test_client_add_embed():
    embed = DiscordEmbed()
    client = DiscordWebhookClient('https://discord.com/api/webhooks/123/abc')
    client.add_embed(embed)
    assert client._payload.embeds == [embed.embed]


def test_client_content():
    client = DiscordWebhookClient('https://discord.com/api/webhooks/123/abc')
    client.content = 'test content'
    assert client._payload.content == 'test content'


def test_client_execute(mocker):
    mocked_response = mocker.Mock(status_code=200)
    mocked_post = mocker.patch(
        'logcaster.discord_utils.discord_client.httpx.post',
        return_value=mocked_response,
    )

    client = DiscordWebhookClient('https://discord.com/api/webhooks/123/abc')
    client.add_embed(DiscordEmbed())
    client.execute()

    mocked_post.assert_called_once()
    assert client._payload is None


@pytest.mark.asyncio
async def test_async_client_execute(mocker):
    mocked_response = mocker.Mock(status_code=200)
    mocked_post = mocker.patch(
        'logcaster.discord_utils.discord_client.httpx.AsyncClient.post',
        return_value=mocked_response,
    )

    client = DiscordWebhookAsyncClient('https://discord.com/api/webhooks/123/abc')
    client.add_embed(DiscordEmbed())
    await client.execute()

    mocked_post.assert_called_once()
    assert client._payload is None
