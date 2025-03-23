from easylog.formatters import TelegramFormatter
from tabulate import tabulate


def test_formatter_returns_a_presto_table(log_record):
    fmt = TelegramFormatter(['message', 'asctime'])
    expected = tabulate([
        ['message', log_record.getMessage()],
        ['asctime', fmt.formatTime(log_record, fmt.datefmt)],
    ], tablefmt='presto', headers=['field', 'value'])
    result = fmt.format(log_record)
    assert result == expected
