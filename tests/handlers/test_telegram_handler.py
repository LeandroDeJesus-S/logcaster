from logcaster.telegram import TelegramHandler


def test_emit(mocker, log_record, mock_telegram_env, capsys):
    mocked_urlopen = mocker.patch('logcaster.telegram.urlopen')
    handler = TelegramHandler()

    emitted = handler.emit(log_record)
    captured = capsys.readouterr()

    mocked_urlopen.assert_called_once()
    assert 'Logging sent to telegram chat id' in captured.out
    assert emitted
