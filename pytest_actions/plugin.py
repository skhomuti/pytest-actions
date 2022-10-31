import os
import sys

import pytest


def pytest_addoption(parser: pytest.Parser, pluginmanager: pytest.PytestPluginManager):
    pass


def pytest_configure(config: pytest.Config):
    pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    report: pytest.TestReport = (yield).get_result()
    if not report.passed:
        path, _, _ = report.location
        if not hasattr(report.longrepr, "reprcrash"):
            return
        lineno = report.longrepr.reprcrash.lineno
        message = report.longrepr.reprcrash.message
        error(path, lineno, report.head_line, message)


def error(path, lineno, testname, message):
    title = f"Test {testname} failed"
    print(f"::error file={path},line={lineno},title={title}::{message}", file=sys.stderr)
