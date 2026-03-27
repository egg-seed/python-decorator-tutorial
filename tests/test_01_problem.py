"""01_problem_without_decorator のテスト。"""

import importlib
import types

import pytest

# 数字始まりのモジュール名は通常の import 構文が使えないため importlib を使用
_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.01_problem_without_decorator"
)


def test_add_returns_correct_result() -> None:
    """Add は正しい足し算の結果を返す。"""
    assert _mod.add(3, 5) == 8


def test_add_with_zero() -> None:
    """Add はゼロを含む加算も正しく動作する。"""
    assert _mod.add(0, 0) == 0
    assert _mod.add(-1, 1) == 0


def test_add_logs_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Add はログ（開始・完了）を出力する。"""
    _mod.add(1, 2)
    captured = capsys.readouterr()
    assert "[開始]" in captured.out
    assert "[完了]" in captured.out
    assert "add" in captured.out


def test_multiply_returns_correct_result() -> None:
    """Multiply は正しい掛け算の結果を返す。"""
    assert _mod.multiply(4, 7) == 28


def test_multiply_logs_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """Multiply はログを出力する。"""
    _mod.multiply(3, 4)
    captured = capsys.readouterr()
    assert "multiply" in captured.out


def test_greet_returns_correct_message() -> None:
    """Greet は正しい挨拶文を返す。"""
    assert _mod.greet("太郎") == "こんにちは、太郎さん！"


def test_greet_different_names() -> None:
    """Greet は異なる名前でも正しく動作する。"""
    assert _mod.greet("花子") == "こんにちは、花子さん！"
    assert _mod.greet("World") == "こんにちは、Worldさん！"
