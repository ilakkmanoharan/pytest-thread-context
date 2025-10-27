import os
import threading
import time
import pytest


def print_current_env(label: str):
    """
    Helper to print the current thread name and PYTEST_CURRENT_TEST + per-thread vars.
    """
    thread_name = threading.current_thread().name
    base = os.environ.get("PYTEST_CURRENT_TEST")
    thread_vars = {k: v for k, v in os.environ.items() if k.startswith("PYTEST_CURRENT_TEST_THREAD_")}
    print(f"[{label}] thread={thread_name}")
    print(f"  PYTEST_CURRENT_TEST={base!r}")
    if thread_vars:
        print(f"  THREAD VARS={thread_vars}")


def run_in_thread(delay=0.1):
    """
    Function to run inside a spawned thread. Waits briefly, then prints env state.
    """
    time.sleep(delay)
    print_current_env("inside thread")


def test_single_thread_env():
    """Baseline: single-thread test."""
    print_current_env("main thread")


def test_multi_thread_env():
    """
    Spawn multiple threads and inspect their environment variables.
    Threads are named pytest-thread-{n} to activate plugin behavior.
    """
    threads = []
    for i in range(3):
        t = threading.Thread(target=run_in_thread, name=f"pytest-thread-{i}")
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def test_pytest_run_from_thread():
    """
    Run pytest.main inside a thread to simulate pytest being launched from a non-main thread.
    """
    def inner_pytest():
        import pytest
        print_current_env("pytest inner thread start")
        pytest.main(["-q", "--maxfail=1", "--disable-warnings", "-k", "single_thread_env"])

    t = threading.Thread(target=inner_pytest, name="pytest-main-thread")
    t.start()
    t.join()
