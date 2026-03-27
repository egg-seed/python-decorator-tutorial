"""07_paramspec_basics のテスト。"""

import importlib
import types

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.07_paramspec_basics"
)


def test_add_untyped_returns_correct_result() -> None:
    """Callable[..., Any] 版 add は正しい結果を返す。"""
    assert _mod.add_untyped(3, 5) == 8


def test_add_typed_returns_correct_result() -> None:
    """ParamSpec 版 add は正しい結果を返す。"""
    assert _mod.add_typed(3, 5) == 8


def test_add_typed_preserves_name() -> None:
    """@log_typed はデコレート後も __name__ を保持する。"""
    assert _mod.add_typed.__name__ == "add_typed"


def test_slow_sum_correct_result() -> None:
    """@timer でデコレートした slow_sum は正しい合計を返す。"""
    assert _mod.slow_sum([1, 2, 3, 4, 5]) == 15


def test_slow_sum_large_list() -> None:
    """slow_sum は大きなリストでも正しく動作する。"""
    numbers = list(range(100))
    assert _mod.slow_sum(numbers) == sum(range(100))
