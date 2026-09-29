# Professional Calculator

A Python command-line calculator with a read-evaluate-print loop (REPL), four arithmetic operations, and session-only calculation history.

## Features

- Addition, subtraction, multiplication, and division
- Operation names, aliases, and symbols:
   - Addition: `add`, `sum`, `+`
   - Subtraction: `subtract`, `minus`, `-`
   - Multiplication: `multiply`, `times`, `*`
   - Division: `divide`, `div`, `/`
- REPL commands: `help`, `history`, and `exit` (`quit` and `q` also exit)
- Input validation for invalid operations, malformed numbers, and non-finite values
- Clear division-by-zero errors
- Calculation instances created through `CalculationFactory`
- Unit tests with 100% statement and branch coverage enforced in CI

## Requirements

- Python 3.11 or newer
- pip

## Setup

Run these commands from the project root. A virtual environment keeps the project dependencies separate from other Python installations.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

If PowerShell blocks activation scripts, allow script execution for the current terminal session, then activate the environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The editable installation installs the runtime dependency and the optional development dependencies (`pytest` and `pytest-cov`).

## Run

Start the calculator from the project root:

```console
python -m app.calculator.cli
```

Choose an operation, then enter two finite numbers when prompted:

```text
Choose an operation: add
Enter the first number: 10
Enter the second number: 5
Result: 15.0
Choose an operation: history
1. 10.0 + 5.0 = 15.0
Choose an operation: exit
Goodbye!
```

Enter `help` to list commands, operations, and aliases. Enter `history` to display successful calculations from the current process; history is not saved after exit. Invalid input displays an error and returns to the operation prompt. Division by zero is rejected without adding a result to history.

## Use the Calculation API

Calculation instances normalize operation names, aliases, and symbols before execution:

```python
from app.calculation import CalculationFactory

calculation = CalculationFactory.create_calculation(12, "*", 3)
print(calculation.calculate())  # 36
```

The `calculate(first_number, operation, second_number)` helper provides the same calculation behavior without retaining a calculation object.

## Project Layout

```text
app/
   calculator/     REPL, command handling, and CLI entry point
   calculation/    Calculation objects, factory, and calculation helpers
   operation/      Arithmetic functions and shared operation metadata
tests/            Pytest unit and CLI integration tests
```

## Run Tests

Run all unit and integration tests:

```console
python -m pytest
```

Measure statement and branch coverage and require both to reach 100%:

```console
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=100
```

Coverage exclusions should be reserved for code that cannot meaningfully be exercised by a test. `# pragma: no cover` excludes the marked line from the report and can exclude an entire conditional clause. `# pragma: no branch` marks a deliberately partial branch as intentional. Prefer adding tests for reachable paths; this project currently needs no coverage exclusions.

## Continuous Integration

The GitHub Actions workflow at `.github/workflows/python-tests.yml` installs the project with development dependencies, runs pytest with branch coverage enabled, and fails if total coverage is below 100%.
