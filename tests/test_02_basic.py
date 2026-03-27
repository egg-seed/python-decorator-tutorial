"""02_basic_decorator のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.02_basic_decorator"
)


def test_add_returns_correct_result() -> None:
    """デコレートされた add は正しい結果を返す。"""
    assert _mod.add(3, 5) == 8


def test_subtract_returns_correct_result() -> None:
    """@構文でデコレートした subtract は正しい結果を返す。"""
    assert _mod.subtract(10, 3) == 7


def test_greet_returns_correct_message() -> None:
    """デコレートされた greet は正しい挨拶を返す。"""
    assert _mod.greet("太郎") == "こんにちは、太郎さん！"


def test_decorator_logs_start_and_end(capsys: pytest.CaptureFixture[str]) -> None:
    """log_decorator は開始・完了ログを出力する。"""
    _mod.add(1, 2)
    captured = capsys.readouterr()
    assert "[開始]" in captured.out
    assert "[完了]" in captured.out


def test_decorator_logs_function_name(capsys: pytest.CaptureFixture[str]) -> None:
    """log_decorator は関数名をログに含める。"""
    _mod.subtract(5, 2)
    captured = capsys.readouterr()
    assert "subtract" in captured.out
