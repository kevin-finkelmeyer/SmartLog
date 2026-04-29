import pandas as pd
import pytest
from smartlog.parser import SmartLogParser


@pytest.fixture
def default_log_file(tmp_path):
    directory = tmp_path / "logs"
    directory.mkdir()
    log_file = directory / "test.log"

    content = """[2026-04-17 01:54:57 [INFO] [auth-service] Running smoothly
[2026-04-17 01:54:57] [INFO] [dns-service] Connected
[2026-04-17 01:54:57] [INFO] [db-service] Running smoothly
[2026-04-17 01:54:57] [INFO] [db-service] Running smoothly
[2026-04-17 01:54:57] [WARNING] [io-service] no responses
[2026-04-17 01:54:57 [INFO] [dns-service] Connected
[2026-04-17 01:54:57] [ERROR] [dns-service] division by zero
[2026-04-17 01:54:57] [WARNING] [db-service Resources low
[2026-04-17 01:54:57] [ERROR] [io-service] division by zero"""
    log_file.write_text(content, encoding="utf-8")

    return log_file


def test_single_valid_line(tmp_path):
    directory = tmp_path / "logs"
    directory.mkdir()

    log_file = directory / "test.log"
    content = "[2024-01-01 12:00:00] [ERROR] [auth-service] Something failed"

    log_file.write_text(content, encoding="utf-8")

    parser = SmartLogParser(str(log_file))

    result = parser.parse()
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == 1
    assert result.shape[1] == 4
    assert result['level'].iloc[0] == 'ERROR'


def test_single_invalid_line(tmp_path):
    directory = tmp_path / "logs"
    directory.mkdir()

    log_file = directory / "test.log"

    content = "2024-01-01 12:00:00] [ERROR] [auth-service] Something failed"

    log_file.write_text(content, encoding="utf-8")

    parser = SmartLogParser(str(log_file))

    result = parser.parse()
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == 0
    assert result.shape[1] == 0
    with pytest.raises(KeyError):
        assert result['level'].iloc[0] == 'ERROR'


def test_empty_file(tmp_path):
    directory = tmp_path / "logs"
    directory.mkdir()

    log_file = directory / "test.log"

    content = ""

    log_file.write_text(content, encoding="utf-8")


    parser = SmartLogParser(str(log_file))

    result = parser.parse()
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == 0
    assert result.shape[1] == 0
    with pytest.raises(KeyError):
        assert result['level'].iloc[0] == 'ERROR'


def test_some_invalid_lines(default_log_file):

    parser = SmartLogParser(str(default_log_file))

    result = parser.parse()
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == 6
    assert result.shape[1] == 4


def test_columns(default_log_file):

    parser = SmartLogParser(str(default_log_file))
    result = parser.parse()

    expected_columns = ['timestamp', 'level', 'service', 'message']
    assert list(result.columns) == expected_columns


def test_timestamp_type(default_log_file):

    parser = SmartLogParser(str(default_log_file))
    result = parser.parse()

    assert pd.api.types.is_datetime64_any_dtype(result['timestamp'])
