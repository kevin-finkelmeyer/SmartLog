import pandas as pd


def test_placeholder():
    assert 1 == 1


def test_single_valid_line(tmp_path):
    directory = tmp_path / "logs"
    directory.mkdir()

    log_file = directory / "test.log"
    content = "[2024-01-01 12:00:00] [ERROR] [auth-service] Something failed"

    log_file.write_text(content, encoding="utf-8")

    from smartlog.parser import SmartLogParser
    parser = SmartLogParser(str(log_file))

    result = parser.parse()
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == 1
    assert result.shape[1] == 4
    assert result['level'].iloc[0] == 'ERROR'
