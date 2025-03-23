from easylog.formatters import BaseFormatter
import pytest


@pytest.mark.parametrize(
    'include,exclude,result',
    [
        (['message', 'asctime'], None, ['message', 'asctime']),
        (['__all__'], None, 'log_record'),
        (None, ['funcName'], ['message', 'asctime']),
    ]
)
def test_get_fields(log_record, include, exclude, result):
    fmt = BaseFormatter(include, exclude)

    log_record.asctime = ''
    log_record.message = ''

    if result == 'log_record':
        result = list(log_record.__dict__.keys())
    if include is None:
        result = [k for k in log_record.__dict__.keys() if k not in exclude]
    
    act_result = list(fmt._get_fields(log_record).keys())
    assert sorted(act_result) == sorted(result)
    