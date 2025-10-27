# pytest-thread-context

A minimal **research playground** to explore how [pytest](https://github.com/pytest-dev/pytest)
manages **test context across multiple threads**.

This project is directly inspired by  
👉 [pytest-dev/pytest#13844](https://github.com/pytest-dev/pytest/issues/13844),
which discusses how to **generalize `PYTEST_CURRENT_TEST`** for multi-threaded test execution.

---

## 🎯 Background

### The problem

`PYTEST_CURRENT_TEST` is a global environment variable set by pytest to indicate which
test (node ID and phase) is currently running.

This works perfectly in **single-threaded** test runs but breaks down under **multi-threading**:
- Multiple tests can be running **simultaneously** in different threads.
- The global env var can only hold **one value**.
- Debuggers or monitoring tools like `htop E` can’t distinguish which thread is executing which test.

---

### Proposed ideas in #13844

| Proposal | Description |
|-----------|-------------|
| **Per-thread env vars** | Give each thread its own env var: `PYTEST_CURRENT_TEST_THREAD_{n}`. |
| **Main-thread-only** | Keep `PYTEST_CURRENT_TEST` for main thread; subthreads unset or separate. |
| **Disable in threading mode** | Avoid misleading results by disabling the env var when multiple threads exist. |
| **New API** | Offer a Python-level `pytest.in_test_run()` or flag like `PYTEST=1`. |

This project allows you to **experiment with those ideas locally**.

---



