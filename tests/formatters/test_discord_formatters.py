from src.formatters import DiscordFormatter

fmt = DiscordFormatter('%(levelname)s - %(message)s')


def test_format_method(log_record):
    """test if the format method returns the correct format"""
    formatted = fmt.format(log_record)
    expected_result = '\U0001f41b DEBUG \U0001f41b - some message'
    assert formatted == expected_result


def test_get_level_name_method(log_record):
    """test if the _get_level_name method return the level name
    in the expected format
    """
    result = fmt._get_level_name(log_record)
    expected_result = '\U0001f41b DEBUG \U0001f41b'
    assert result == expected_result


def test_get_emoji(log_record):
    """test if the _get_emoji method returns the correct emoji"""
    result = fmt._get_emoji(log_record)
    expected_result = '\U0001f41b'
    assert result == expected_result
