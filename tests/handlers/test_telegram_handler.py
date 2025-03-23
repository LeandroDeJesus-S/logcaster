from logcaster.telegram import TelegramHandler


def test_emit(mocker, log_record):
    mocked_urlopen = mocker.patch('logcaster.telegram.urlopen')
    handler = TelegramHandler()
    emitted = handler.emit(log_record)
    mocked_urlopen.assert_called_once()
    assert emitted
