# Project Context: log-report-generator

## Purpose

`log-report-generator` is a small Python CLI portfolio project that will parse
application logs and generate CSV reports. It is intended to demonstrate skills
relevant to small freelance jobs involving Python scripts, log analysis, file
processing, data conversion, reports, and simple command-line tools.

The owner has about 2.5 years of commercial C++ experience at Nokia, working on
5G base-station software with C++17, Linux, GoogleTest, Git/Gerrit,
Jenkins/Zuul, log analysis, troubleshooting, and functional testing. They can
write small Python tools but do not want to present themselves as a Python
expert.

The learning process matters as much as the finished project. Development must
continue in small, understandable stages.

## Collaboration style

Act as a mentor and code reviewer.

- Explain each decision before adding code.
- Suggest small steps.
- Encourage the owner to implement parts and then review their work.
- Generate only code required by the current step.
- Ask the owner to run tests or paste their output after each stage.
- Prefer simplicity, readability, testability, and explicit names.
- Avoid excessive abstraction and unnecessary dependencies.
- Use type hints when helpful.
- Test behavior rather than implementation details.
- Treat malformed log input as expected data that should be handled cleanly.

Prefer the Python standard library, especially `argparse`, `pathlib`, `re`,
`datetime`, `csv`, `collections`, and `dataclasses`. Tests use `pytest`.

## MVP requirements

Eventually, the program should:

1. Read a text log file.
2. Recognize entries in this format:

   ```text
   YYYY-MM-DD HH:MM:SS LEVEL MESSAGE
   ```

   Example:

   ```text
   2026-06-24 14:32:10 ERROR Database connection failed
   ```

3. Support `INFO`, `WARNING`, and `ERROR`.
4. Skip empty lines.
5. Detect and count malformed lines.
6. Filter entries by log level.
7. Filter entries by date range.
8. Group identical messages by `(log_level, message)`.
9. Count occurrences.
10. Determine the first and last occurrence of each message.
11. Generate a CSV report.
12. Print a short terminal summary.
13. Include pytest tests.
14. Include a README with usage instructions.

## Out of scope for the MVP

- GUI or web application
- HTML reports or charts
- Database
- `pandas`
- Multiple log formats
- Multiline stack-trace parsing
- Directory processing
- API integration
- Advanced YAML/JSON configuration
- Other speculative features not required by the MVP

## Planned final structure

```text
log-report-generator/
├── README.md
├── pyproject.toml
├── .gitignore
├── LICENSE
├── examples/
│   └── application.log
├── src/
│   └── log_report/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── models.py
│       ├── parser.py
│       └── report.py
└── tests/
    ├── test_parser.py
    ├── test_filtering.py
    ├── test_report.py
    └── test_cli.py
```

This is the eventual destination, not a request to create everything at once.

## Current stage boundary

Only parser-stage work is authorized:

1. Repository structure
2. `examples/application.log`
3. `LogEntry`
4. `parse_log_line(line: str) -> LogEntry | None`
5. Parser tests

Do not start the CLI, CSV generation, filtering, aggregation, or report code
until the parser stage is reviewed and declared complete.

## Repository state on 2026-08-24

Remote:

```text
git@github.com:rotens/log-report-generator.git
```

The active branch is `main`. The latest parser implementation commit is
`e301246`:

```text
Tighten log line validation
```

That commit is local until it is pushed to GitHub. The context document is
committed separately after being updated.

Current project-facing files:

```text
log-report-generator/
├── .gitignore
├── LICENSE
├── PROJECT_CONTEXT.md
├── README.md
├── pyproject.toml
├── examples/                  # currently empty
├── src/
│   └── log_report/
│       ├── __init__.py
│       ├── models.py
│       └── parser.py
└── tests/
    └── test_parser.py
```

Push all local commits before moving to another computer.

Generated/local files such as `.venv/`, `.pytest_cache/`, `*.egg-info/`,
`__pycache__/`, and Python bytecode must remain ignored.

## Packaging and test configuration

`pyproject.toml` uses:

- `setuptools>=68` and `setuptools.build_meta`
- Distribution name `log-report-generator`
- Version `0.1.0`
- Python `>=3.10`
- No runtime dependencies
- Optional development dependency `pytest>=8`
- Package discovery under `src`
- Test discovery under `tests`
- Pytest option `-ra`

Install the editable project with development dependencies using:

```bash
python -m pip install -e ".[dev]"
```

The distribution name uses a hyphen. Python imports use the package name with
an underscore:

```python
from log_report.parser import parse_log_line
```

## Completed parser work

`src/log_report/models.py` defines:

```python
@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    log_level: str
    message: str
```

The immutable dataclass provides generated initialization, representation, and
value equality. The explicit name `log_level` was chosen instead of `level`;
use it consistently later.

`src/log_report/parser.py` provides:

```python
parse_log_line(line: str) -> LogEntry | None
```

Current behavior:

- Removes Unix and Windows line endings with `rstrip("\r\n")`.
- Returns `None` for empty and whitespace-only lines.
- Rejects other leading or trailing whitespace.
- Uses `split(maxsplit=3)` to obtain date, time, log level, and message while
  preserving a multi-word message.
- Returns `None` if all four fields are not present.
- Accepts only `INFO`, `WARNING`, and `ERROR`.
- Stores accepted levels in `SUPPORTED_LOG_LEVELS`.
- Enforces the fixed-width timestamp shape with a compiled regular expression.
- Parses timestamps using `datetime.strptime()` with
  `%Y-%m-%d %H:%M:%S` to validate calendar values.
- Returns `None` for an invalid timestamp, including impossible dates and
  non-zero-padded components.
- Returns a `LogEntry` for valid input.

`tests/test_parser.py` covers:

- A complete valid `ERROR` line and the resulting `LogEntry`.
- Empty and whitespace-only input.
- A missing message.
- An impossible date.
- An unsupported `DEBUG` level.
- Parameterized acceptance of `INFO`, `WARNING`, and `ERROR`.
- A timestamp with a non-zero-padded month.
- Excluding a trailing newline from the parsed message.
- Rejection of leading and trailing whitespace.

The supported-level test uses `pytest.mark.parametrize`. Plain test functions
and ordinary `assert` statements do not require importing pytest; direct use of
the parameterization decorator does.

Verified baseline on 2026-08-24:

```text
platform linux -- Python 3.12.3, pytest-9.1.1
collected 13 items
tests/test_parser.py ............. [100%]
13 passed in 0.12s
```

## Continue on a laptop

The remote uses SSH. The laptop must have a GitHub-authorized SSH key. Verify
authentication:

```bash
ssh -T git@github.com
```

Clone and set up the project on Linux or macOS:

```bash
git clone git@github.com:rotens/log-report-generator.git
cd log-report-generator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

If SSH is not configured on the laptop, clone over HTTPS instead:

```bash
git clone https://github.com/rotens/log-report-generator.git
```

The `.venv` directory is intentionally not transferred between computers. It
is platform-specific and should be recreated using `pyproject.toml`.

## Recommended next steps

Stay within the parser stage:

1. Add the already-designed parameterized test that rejects double spaces and
   tab separators between structural fields. The current implementation still
   uses whitespace-based `split(maxsplit=3)` and accepts those inputs.
2. Make the smallest parser change needed to require single-space structural
   separators while continuing to allow spaces inside the message.
3. Expand the zero-padding test to cover day, hour, minute, and second as well
   as month, preferably with `pytest.mark.parametrize`.
4. Add a small `examples/application.log` with representative valid, empty,
   and malformed lines.
5. Run `git diff --check` and the complete parser suite:

   ```bash
   git diff --check
   python -m pytest
   ```

Only after reviewing and completing the parser stage should work begin on
whole-file parsing and malformed-line counting. CLI, filtering, aggregation,
and CSV reporting remain out of scope.

## Before continuing on the laptop

Push both the parser commit and this context update:

```bash
git push
```

Then confirm that the laptop checks out `main`, recreate its virtual
environment, install `.[dev]`, and run the test suite before making changes.
