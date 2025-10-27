import os
import pytest
from . import plugin_thread_env  # auto-load the experimental plugin

pytest_plugins = [plugin_thread_env]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """
    Hook into pytest's runtest protocol to log PYTEST_CURRENT_TEST and per-thread vars
    before and after each test.
    """
    before_global = os.environ.get("PYTEST_CURRENT_TEST", "")
    before_thread = [
        (k, v) for k, v in os.environ.items() if k.startswith("PYTEST_CURRENT_TEST_THREAD_")
    ]

    outcome = yield

    after_global = os.environ.get("PYTEST_CURRENT_TEST", "")
    after_thread = [
        (k, v) for k, v in os.environ.items() if k.startswith("PYTEST_CURRENT_TEST_THREAD_")
    ]

    print(f"\n[pytest_runtest_protocol] {item.nodeid}")
    print(f"  GLOBAL BEFORE={before_global}")
    print(f"  GLOBAL AFTER ={after_global}")
    if before_thread or after_thread:
        print(f"  THREAD VARS BEFORE={before_thread}")
        print(f"  THREAD VARS AFTER ={after_thread}")
