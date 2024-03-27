import datetime
import sys
from typing import Optional, TextIO

from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.terminal import TerminalReporter
import pytest


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("Adds a timestamp format to pytest output. Currently only works in verbose mode.")
    group.addoption("--datefmt", help="Format that is compatible with `strftime`", default="%Y-%m-%d %H:%M:%S")
    group.addoption(
        "--prefixfmt",
        help="Format for prefix. Has access to fields: ['formatted_datetime']",
        default="[{formatted_datetime}] ",
    )


class TimestamperTerminalReporter(TerminalReporter):
    def __init__(self, config: Config, file: Optional[TextIO] = None) -> None:
        super().__init__(config, file)

        # we need a cache to ensure we only print one line per test
        self._cache = {}

    def _locationline(self, nodeid: str, fspath: str, lineno: Optional[int], domain: str):
        key = (nodeid, fspath, lineno, domain)
        if key not in self._cache:
            baseline = super()._locationline(nodeid, fspath, lineno, domain)
            formatted_datetime = datetime.datetime.now().strftime(self.config.option.datefmt)
            formatted_prefix = self.config.option.prefixfmt.format(formatted_datetime=formatted_datetime)
            self._cache[key] = formatted_prefix + baseline
        return self._cache[key]


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    if config.pluginmanager.has_plugin("terminalreporter"):
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        config.pluginmanager.unregister(reporter, "terminalreporter")
        config.pluginmanager.register(TimestamperTerminalReporter(config, sys.stdout), "terminalreporter")
