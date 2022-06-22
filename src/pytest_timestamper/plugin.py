import datetime
import sys
from typing import Optional, TextIO

import pytest
from _pytest.config import Config
try:
    from _pytest.config.argparsing import Parser
except ImportError:
    from _pytest.config import Parser
from _pytest.terminal import TerminalReporter


def pytest_addoption(parser):
    # type: (Parser) -> None
    group = parser.getgroup("Adds a timestamp format to pytest output. Currently only works in verbose mode.")
    group.addoption("--datefmt", help="Format that is compatible with `strftime`", default="%Y-%m-%d %H:%M:%S")
    group.addoption(
        "--prefixfmt",
        help="Format for prefix. Has access to fields: ['formatted_datetime']",
        default="[{formatted_datetime}] ",
    )


class TimestamperTerminalReporter(TerminalReporter):
    def __init__(self, config, file = None):
        # type: (Config, Optional[TextIO]) -> None
        if sys.version_info[0] == 2:
            TerminalReporter.__init__(self, config, file)
        else:
            super().__init__(config, file)

        # we need a cache to ensure we only print one line per test
        self._cache = {}

    def _locationline(self, nodeid, fspath, lineno, domain):
        # type: (str, str, Optional[int], str) -> None
        key = (nodeid, fspath, lineno, domain)
        if key not in self._cache:
            if sys.version_info[0] == 2:
                baseline = TerminalReporter._locationline(self, nodeid, fspath, lineno, domain)
            else:
                baseline = super()._locationline(nodeid, fspath, lineno, domain)
            formatted_datetime = datetime.datetime.now().strftime(self.config.option.datefmt)
            formatted_prefix = self.config.option.prefixfmt.format(formatted_datetime=formatted_datetime)
            self._cache[key] = formatted_prefix + baseline
        return self._cache[key]


@pytest.mark.trylast
def pytest_configure(config):
    # type: (Config) -> None
    if not hasattr(config.pluginmanager, 'has_plugin'):
        config.pluginmanager.has_plugin = config.pluginmanager.hasplugin
    if config.pluginmanager.has_plugin("terminalreporter"):
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        config.pluginmanager.unregister(reporter, "terminalreporter")
        config.pluginmanager.register(TimestamperTerminalReporter(config, sys.stdout), "terminalreporter")
