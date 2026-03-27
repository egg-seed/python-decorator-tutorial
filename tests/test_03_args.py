"""03_decorator_with_args のテスト。"""

import importlib
import types

import pytest

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.03_decorator_with_args"
)


def test_repeat_executes_correct_times(capsys: pytest.CaptureFixture[str]) -> None:
    """@repeat(times=3) は関数を 3 回実行する。"""
    _mod.say_hello()
    captured = capsys.readouterr()
    # 「こんにちは！」が 3 回出力される
    assert captured.out.count("こんにちは！") == 3


def test_repeat_shows_count(capsys: pytest.CaptureFixture[str]) -> None:
    """@repeat は (n/total 回目) のカウントを表示する。"""
    _mod.say_hello()
    captured = capsys.readouterr()
    assert "(1/3回目)" in captured.out
    assert "(3/3回目)" in captured.out


def test_fetch_data_logs_level(capsys: pytest.CaptureFixture[str]) -> None:
    """@log_with_level(level='DEBUG') は DEBUG レベルのログを出す。"""
    _mod.fetch_data("https://example.com")
    captured = capsys.readouterr()
    assert "[DEBUG]" in captured.out


def test_delete_user_logs_warning(capsys: pytest.CaptureFixture[str]) -> None:
    """@log_with_level(level='WARNING') は WARNING レベルのログを出す。"""
    _mod.delete_user(1)
    captured = capsys.readouterr()
    assert "[WARNING]" in captured.out
