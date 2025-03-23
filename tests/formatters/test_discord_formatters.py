from logcaster.formatters import DiscordFormatter
from discord_webhook import DiscordEmbed

fmt = DiscordFormatter()


def test_format_method_returns_an_embed_instance(log_record):
    """test if the format method returns an instance of DiscordEmbed class"""
    formatted = fmt.format(log_record)
    assert isinstance(formatted, DiscordEmbed)


def test_get_level_name_method(log_record):
    """test if the _get_level_name method return the level name
    in the expected format
    """
    result = fmt._get_level_name_with_emoji(log_record)
    expected_result = '\U0001f41b DEBUG \U0001f41b'
    assert result == expected_result


def test_get_emoji(log_record):
    """test if the _get_emoji method returns the correct emoji"""
    result = fmt._get_emoji(log_record)
    expected_result = '\U0001f41b'
    assert result == expected_result
