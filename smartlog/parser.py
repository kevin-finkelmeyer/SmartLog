import re
from pathlib import Path

import pandas as pd

log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class SmartLogParser:
    def __init__(self, filename):
        self.path = Path(filename)
        self.regex_pattern = "\\[(?P<timestamp>.+?)\\] \\[(?P<level>.+?)\\] \\[(?P<service>.+?)\\] (?P<message>.+)"
        self.data: pd.DataFrame = pd.DataFrame()

    def parse(self) -> pd.DataFrame:
        # Check for File existence
        if not self.path.exists():
            raise FileNotFoundError(self.path)

        rows = []
        with open(self.path) as f:
            for line in f:
                match = re.match(self.regex_pattern, line)
                if match:
                    rows.append(match.groupdict())
                else:
                    print(f"Failed to parse line: {line}")

            if len(rows) == 0:
                return pd.DataFrame()

            self.data = pd.DataFrame(rows)
            # Change datetype of timestamp to datetime
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            # Change datetype of level to category
            self.data['level'] = pd.Categorical(self.data['level'], log_levels, ordered=True)

            return self.data


if __name__ == "__main__":
    parser = SmartLogParser("../data/sample.log")
    print(parser.parse())
