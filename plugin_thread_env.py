"""
pytest-thread-context: experimental plugin to simulate per-thread test context env vars.

Implements the idea proposed in pytest-dev/pytest#13844:
Each thread named 'pytest-thread-{n}' gets its own env var:

    PYTEST_CURRENT_TEST_THREAD_{n} = "<nodeid> (<phase>)"

The main thread still uses the standard PYTEST_CURRENT_TEST variable.
"""

import os
import re
import threading
import pytest

# Pattern to match pytest-thread-{n}
THREAD_NAME_PATTERN = re.compile(r"^pytest-thread-(\d+)$")


def _thread_var_name():
    """
    Return the appropriate environment variable name for the current thread.
    - For main thread: PYTEST_CURRENT_TEST
    - For pytest-thread-{n}: PYTEST_CURRENT_TEST_THREAD_{n}
    """
    tname = threading.current_thread().name
    m = THREAD_NAME_PATTERN.match(tname)
    if m:
        return f"PYTEST_CURRENT_TEST_THREAD_{m.group(1)}"
    return "PYTEST_CURRENT_TEST"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """
    Wrap the test protocol to set thread-aware env vars.
    """
    var_name = _thread_var_name()
    nodeid = item.nodeid
    phase = "setup"

    # Set env var before setup
    os.environ[var_name] = f"{nodeid} ({phase})"
    yield

    # After test, cleanup
    if var_name != "PYTEST_CURRENT_TEST":
        del os.environ[var_name]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """
    During the actual test call phase, set the appropriate env var for the thread.
    """
    var_name = _thread_var_name()
    nodeid = item.nodeid
    os.environ[var_name] = f"{nodeid} (call)"
    outcome = yield
    # cleanup handled in protocol hook


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    """
    During teardown, set the env var to indicate teardown phase.
    """
    var_name = _thread_var_name()
    nodeid = item.nodeid
    os.environ[var_name] = f"{nodeid} (teardown)"
    yield


def pytest_report_header(config):
    """
    Add a short note to pytest header to indicate the plugin is active.
    """
    return "pytest-thread-context plugin: per-thread env var simulation enabled"
