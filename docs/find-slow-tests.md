# find-slow-tests

This doc describes how to find tests that are slow because they wait (sleeps, retries, real network,
subprocesses) using pytest-slowtrace, fix them, and measure the wall-time change

# Find slow tests with pytest-slowtrace

Slow suites usually have a few tests that sit idle: a retry with backoff, a real HTTP call, a `sleep`.
`pytest-slowtrace` reports tests that took at least 0.2s and were at least 50% idle, with the
application line they were waiting in. CPU-bound slowness is not reported; use a profiler for that.

Do this separately from parallelism advice (`pytest-xdist`). xdist overlaps waits instead of removing
them, and it makes per-test timing noisy. Remove the waits first; consider xdist afterwards.

## 1. Try it without changing the project

Install into the existing tox env. Do not edit `tox.ini` or requirements yet:

```
uv pip install --python .tox/<env>/bin/python pytest-slowtrace
```

Tox recreates the env when deps change, which discards this install. That is fine.

Run pytest directly from the env, serially, bypassing the `commands` in tox.ini (which may add `-n`, `--cov`):

```
.tox/<env>/bin/python -m pytest -q -p no:cacheprovider tests/ --slowtrace-app-packages=<package>,tests
```

Always pass `--slowtrace-app-packages`. Without it, "application code" means anything under the root
directory, and `.tox/` is under the root, so the report blames `urllib3` or `anyio` instead of your code.

Record the baseline: `time` the same command, three runs.

## 2. Read the report

Each line is `seconds (cpu%) test -- mostly at file:line in function`. Sort out what each one is waiting on:

- **Retry or backoff in code under test** (`_backoff_timer`, `time.sleep`): patch the sleep, the retry
  count, or the function that makes the call.
- **Real network or subprocess the test does not need**: replace it with a fake at the narrowest seam.
  Patch the method that returns data, not `requests`.
- **Intentional integration test** (calls a real service): leave it, and mark it
  `@pytest.mark.xslowtrace` so it stops appearing. Say in a comment what it calls.
- **Fixture or thread wait** (`threading.py ... in wait`): look at what the   thread is blocked on;
  often the same real call, one level up.

Fix the largest first. A patch that stubs too much can make a test pass without testing anything: keep
the assertions that motivated the test.

## 3. Change deps only if you found something

If the report was empty or only intentional integration tests, stop and say so.
Do not add a dependency for nothing.

If you fixed tests, add `pytest-slowtrace` to the project's test deps (typically the `deps` in `tox.ini`)
so regressions show up in CI, and set `--slowtrace-app-packages=<package>,tests` in `addopts`.

## 4. Report the change

Rerun the three timed runs and report before and after, per test and for the suite. Timing on a loaded
machine is noisy; say so if runs overlap. List which tests were fixed, which were marked `xslowtrace`,
and which remain slow.
