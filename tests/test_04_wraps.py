"""04_functools_wraps のテスト。"""

import importlib
import types

_mod: types.ModuleType = importlib.import_module(
    "decorator_tutorial.04_functools_wraps"
)


def test_without_wraps_name_is_wrapper() -> None:
    """@wraps なしのデコレータは __name__ が 'wrapper' になる。"""
    assert _mod.add_bad.__name__ == "wrapper"


def test_with_wraps_preserves_name() -> None:
    """@wraps ありのデコレータは __name__ が元の関数名のまま。"""
    assert _mod.add_good.__name__ == "add_good"


def test_with_wraps_preserves_docstring() -> None:
    """@wraps ありのデコレータは __doc__ を保持する。"""
    assert _mod.add_good.__doc__ is not None
    assert "足し算" in _mod.add_good.__doc__


def test_add_bad_returns_correct_result() -> None:
    """@wraps なし版も計算結果は正しい。"""
    assert _mod.add_bad(3, 5) == 8


def test_add_good_returns_correct_result() -> None:
    """@wraps あり版も計算結果は正しい。"""
    assert _mod.add_good(3, 5) == 8
