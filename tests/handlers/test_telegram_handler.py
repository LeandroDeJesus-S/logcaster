from easylog.handlers import TelegramHandler


def test_emit(mocker, log_record):
    mocked_urlopen = mocker.patch('easylog.handlers.urlopen')
    handler = TelegramHandler()
    emitted = handler.emit(log_record)
    mocked_urlopen.assert_called_once()
    assert emitted
