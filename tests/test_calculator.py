import importlib
import runpy
import sys

# This module tests interactive CLI behavior and the script entry points from the user's perspective.


def test_run_interactive_handles_valid_and_invalid_operations(monkeypatch, capsys):
    responses = iter(["add", "5", "3", "divide", "10", "0", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    calculate_and_print = False
    try:
        from app.calculator.calculator import run_interactive

        run_interactive()
        calculate_and_print = True
    except Exception:
        pass

    captured = capsys.readouterr()
    assert calculate_and_print is True
    assert "Interactive Calculator" in captured.out
    assert "Result: 8.0" in captured.out or "Result: 8" in captured.out
    assert "Cannot divide by zero" in captured.out


def test_run_interactive_help_history_and_exit(monkeypatch, capsys):
    responses = iter(["help", "history", "add", "4", "2", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    from app.calculator.calculator import run_interactive

    run_interactive()

    captured = capsys.readouterr()
    assert "Commands: help, history, exit" in captured.out
    assert "No calculations in history." in captured.out
    assert "1. 4.0 + 2.0 = 6.0" in captured.out
    assert "Goodbye!" in captured.out


def test_run_interactive_handles_end_of_input(monkeypatch, capsys):
    def raise_eof(prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)

    from app.calculator.calculator import run_interactive

    run_interactive()

    assert "Goodbye!" in capsys.readouterr().out


def test_run_interactive_invalid_operation_shows_available_choices(monkeypatch, capsys):
    responses = iter(["sqrt", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    from app.calculator.calculator import run_interactive

    run_interactive()

    captured = capsys.readouterr()
    assert "Invalid operation" in captured.out
    assert "add (+)" in captured.out
    assert "subtract (-)" in captured.out
    assert "multiply (*)" in captured.out
    assert "divide (/)." in captured.out


def test_run_interactive_rejects_non_finite_numbers(monkeypatch, capsys):
    responses = iter(["add", "nan", "5", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    from app.calculator.calculator import run_interactive

    run_interactive()

    captured = capsys.readouterr()
    assert "Please enter a finite number" in captured.out


def test_run_interactive_invalid_number_prompts_user_again(monkeypatch, capsys):
    responses = iter(["add", "abc", "5", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    from app.calculator.calculator import run_interactive

    run_interactive()

    captured = capsys.readouterr()
    assert "Invalid first number" in captured.out
    assert "Please enter a valid number" in captured.out


def test_cli_module_runs_main(monkeypatch):
    called = {"run": False}

    def fake_run_interactive():
        called["run"] = True

    import app.calculator.calculator as calculator_module

    monkeypatch.setattr(calculator_module, "run_interactive", fake_run_interactive)
    sys.modules.pop("app.calculator.cli", None)
    runpy.run_module("app.calculator.cli", run_name="__main__")

    assert called["run"] is True


def test_cli_module_import_does_not_run_interactive(monkeypatch):
    called = {"run": False}

    def fake_run_interactive():
        called["run"] = True

    import app.calculator.calculator as calculator_module

    monkeypatch.setattr(calculator_module, "run_interactive", fake_run_interactive)
    sys.modules.pop("app.calculator.cli", None)
    cli_module = importlib.import_module("app.calculator.cli")

    assert called["run"] is False
    assert cli_module.run_interactive is fake_run_interactive


def test_calculator_module_runs_main(monkeypatch, capsys):
    responses = iter(["quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    sys.modules.pop("app.calculator.calculator", None)
    runpy.run_module("app.calculator.calculator", run_name="__main__")

    captured = capsys.readouterr()
    assert "Interactive Calculator" in captured.out
    assert "Goodbye!" in captured.out
